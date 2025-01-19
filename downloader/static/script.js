async function downloadVideo() {
  const url = document.getElementById("videoUrl").value;
  const message = document.getElementById("message");

  // Use dynamic base URL
  const baseUrl = window.location.origin;
  const endpoint = `${baseUrl}/api/download/`;

  console.log("JS: Sending download request to:", endpoint);

  message.textContent = "Downloading...";

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url }),
    });

    const data = await response.json();

    if (response.ok) {
      console.log("JS: Video download URL received:", data.download_url);

      // Automatically download the video
      const a = document.createElement("a");
      a.href = data.download_url; // Cloudinary URL
      a.download = "video.mp4"; // Suggested file name
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      console.log("JS: Video downloaded successfully!");
      message.textContent = "Download completed!";
    } else {
      console.error("JS: Download failed:", data.error);
      message.textContent = data.error || "Download failed.";
    }
  } catch (error) {
    console.error("JS: An error occurred:", error);
    message.textContent = "An error occurred.";
  }
}
