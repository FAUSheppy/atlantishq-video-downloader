chrome.action.onClicked.addListener(async (tab) => {

    if (!tab.url) {
        console.error("No active tab URL found.");
        return;
    }

    //const host = "https://downloader.atlantishq.de/submit-url"
    const host = "http://localhost:5000/submit-url"
    const token = "test"
    const targetUrl = `${host}?secret=${token}&url=${encodeURIComponent(tab.url)}`;
  
    try {
        await fetch(targetUrl, { method: 'GET' });
        console.log(`Submitted URL: ${targetUrl}`);
    } catch (error) {
        console.error(`Error submitting URL: ${error}`);
    }

});
