const API_BASE_URL = "http://localhost:8000"

export async function uploadImages(files) {
  const formData = new FormData()
  files.forEach(file => formData.append("files", file))
  return fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData
  })
}

export async function searchImage(file, topK) {
  const formData = new FormData()
  formData.append("file", file)
  return fetch(`${API_BASE_URL}/search?topK=${topK}`, {
    method: "POST",
    body: formData
  })
}
