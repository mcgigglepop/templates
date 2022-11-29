package render

import (
	"bytes"
	"log"
	"net/http"
	"path/filepath"
	"text/template"

	"github.com/mcgigglepop/golang-aws-password-manager/pkg/config"
	"github.com/mcgigglepop/golang-aws-password-manager/pkg/models"
)

var app *config.AppConfig

// NewTemplates sets the config for the new template package
func NewTemplates(a *config.AppConfig) {
	app = a
}

func AddDefaultData(td *models.TemplateData) *models.TemplateData {

	return td
}

// RenderTemplate renders templates using html/template
func RenderTemplate(w http.ResponseWriter, tmpl string, td *models.TemplateData) {

	var tc map[string]*template.Template

	if app.UseCache {
		// get the template cache from the app config
		tc = app.TemplateCache
	} else {
		tc, _ = CreateTemplateCache()
	}

	// get requested template from cache
	t, ok := tc[tmpl]
	if !ok {
		log.Fatal("Could not get template from template cache")
	}

	buf := new(bytes.Buffer)

	td = AddDefaultData(td)

	_ = t.Execute(buf, td)

	// render the template
	_, err := buf.WriteTo(w)
	if err != nil {
		log.Println(err)
	}
}

func CreateTemplateCache() (map[string]*template.Template, error) {
	// create a map of pointers to template
	myCache := map[string]*template.Template{}

	// get all of the files *.page.tmpl from the templates folder
	pages, err := filepath.Glob("./templates/*.page.tmpl")
	if err != nil {
		return myCache, err
	}

	// range through all files ending in .page.tmpl
	for _, page := range pages {
		// page is full path so we want to strip off path leaving file name
		name := filepath.Base(page)

		// give template a name and parse the page file
		ts, err := template.New(name).ParseFiles(page)
		if err != nil {
			return myCache, err
		}

		// look fir layout files first
		matches, err := filepath.Glob("./templates/*.layout.tmpl")
		if err != nil {
			return myCache, err
		}

		// if matches
		if len(matches) > 0 {
			ts, err = ts.ParseGlob("./templates/*.layout.tmpl")
			if err != nil {
				return myCache, err
			}
		}
		// add to map
		myCache[name] = ts
	}

	return myCache, nil
}
