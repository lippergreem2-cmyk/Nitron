// Package organize_files_test contains tests for organizing_files.
package organize_files_test

import (
	"testing"
	"os"
	"fsnotify"
	"time"
	"path/filepath"
)

// TestOrganizeFiles checks that the organize_files function works correctly.