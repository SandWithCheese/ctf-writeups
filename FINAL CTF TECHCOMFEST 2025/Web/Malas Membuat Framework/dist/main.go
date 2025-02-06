package main

import (
	"crypto/rand"
	"embed"
	"encoding/base64"
	"log"
	"net/http"
	"os"
	"strings"
	"sync"
	"text/template"
)

//go:embed index.html
var content embed.FS

var (
	nonces     = make(map[string]string)
	noncesLock sync.Mutex
)

func generateNonce() (string, error) {
	nonce := make([]byte, 16)
	if _, err := rand.Read(nonce); err != nil {
		return "", err
	}
	return base64.StdEncoding.EncodeToString(nonce), nil
}

func handler(w http.ResponseWriter, r *http.Request) {
	tmpl, err := template.ParseFS(content, "index.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	r.URL.Path = r.URL.Path[1:]
	if strings.Contains(strings.ToLower(r.URL.Path), "</title") {
		http.Error(w, "Not Found", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "text/html")
	err = tmpl.Execute(w, r)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func adminHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodGet {
		nonce, err := generateNonce()
		if err != nil {
			http.Error(w, "Failed to generate nonce", http.StatusInternalServerError)
			return
		}

		// Store the nonce in the map
		noncesLock.Lock()
		nonces[nonce] = nonce
		noncesLock.Unlock()

		tmpl, err := template.New("admin").Parse(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Admin Page</title>
        </head>
        <body>
            <form action="/admin/" method="POST">
                <input type="hidden" name="nonce" value="{{.Nonce}}">
                <!-- Your other form fields here -->
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>`)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		data := struct {
			Nonce string
		}{
			Nonce: nonce,
		}

		err = tmpl.Execute(w, data)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
		}
	} else if r.Method == http.MethodPost {
		// Verify the nonce
		nonce := r.FormValue("nonce")
		noncesLock.Lock()
		if _, exists := nonces[nonce]; !exists {
			noncesLock.Unlock()
			http.Error(w, "Invalid CSRF token", http.StatusForbidden)
			return
		}
		delete(nonces, nonce) // Use once and delete

		noncesLock.Unlock()

		// get flag from env
		flag := os.Getenv("FLAG")
		// Your admin logic here
		w.Write([]byte("Admin action performed successfully here is your flag: " + flag))
	}
}

func main() {
	http.HandleFunc("/admin/", adminHandler)
	http.HandleFunc("/", handler)
	log.Println("Server is listening on port 8081...")
	err := http.ListenAndServe("127.0.0.1:8081", nil)
	if err != nil {
		log.Fatal(err)
	}
}
