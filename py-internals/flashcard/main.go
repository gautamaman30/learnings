package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path/filepath"
)

type Card struct {
	Key   string `json:"key"`
	Value string `json:"value"`
}

type FlashcardData struct {
	Groups map[string][]Card `json:"groups"`
}

const dataFile = "flashcards.json"

var flashcards FlashcardData

// Load data from JSON file
func loadData() error {
	if _, err := os.Stat(dataFile); os.IsNotExist(err) {
		// File doesn't exist, create with empty data
		flashcards = FlashcardData{Groups: make(map[string][]Card)}
		return saveData()
	}

	data, err := ioutil.ReadFile(dataFile)
	if err != nil {
		return err
	}

	if len(data) == 0 {
		flashcards = FlashcardData{Groups: make(map[string][]Card)}
		return nil
	}

	return json.Unmarshal(data, &flashcards)
}

// Save data to JSON file
func saveData() error {
	data, err := json.MarshalIndent(flashcards, "", "  ")
	if err != nil {
		return err
	}
	return ioutil.WriteFile(dataFile, data, 0644)
}

// Enable CORS
func enableCORS(w http.ResponseWriter) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
}

// Handle preflight requests
func handlePreflight(w http.ResponseWriter, r *http.Request) {
	if r.Method == "OPTIONS" {
		enableCORS(w)
		w.WriteHeader(http.StatusOK)
		return
	}
}

// Get all flashcard data
func getFlashcards(w http.ResponseWriter, r *http.Request) {
	enableCORS(w)
	if r.Method == "OPTIONS" {
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(flashcards.Groups)
}

// Save flashcard data
func saveFlashcards(w http.ResponseWriter, r *http.Request) {
	enableCORS(w)
	if r.Method == "OPTIONS" {
		return
	}

	if r.Method != "POST" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var newGroups map[string][]Card
	if err := json.NewDecoder(r.Body).Decode(&newGroups); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	flashcards.Groups = newGroups
	if err := saveData(); err != nil {
		http.Error(w, "Error saving data", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "success"})
}

// Serve static files
func serveStaticFile(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path == "/" {
		r.URL.Path = "/index.html"
	}
	
	// Remove leading slash for file path
	filePath := r.URL.Path[1:]
	
	// Security check - prevent directory traversal
	if filepath.IsAbs(filePath) || filepath.Clean(filePath) != filePath {
		http.Error(w, "Invalid file path", http.StatusBadRequest)
		return
	}
	
	// Check if file exists
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		http.Error(w, "File not found", http.StatusNotFound)
		return
	}
	
	http.ServeFile(w, r, filePath)
}

func main() {
	// Load existing data
	if err := loadData(); err != nil {
		log.Printf("Error loading data: %v", err)
		flashcards = FlashcardData{Groups: make(map[string][]Card)}
	}

	// API routes
	http.HandleFunc("/api/flashcards", getFlashcards)
	http.HandleFunc("/api/save", saveFlashcards)

	// Serve static files
	http.HandleFunc("/", serveStaticFile)

	fmt.Println("Server starting on http://localhost:8080")
	fmt.Println("Flashcard data will be saved to:", dataFile)
	log.Fatal(http.ListenAndServe(":8080", nil))
}