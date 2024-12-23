chrome.action.onClicked.addListener(async (tab) => {

    if (!tab.url) {
        console.error("No active tab URL found.");
        return;
    }

    const targetUrl = `https://downloader.atlantishq.de?secret=token&url=${encodeURIComponent(tab.url)}`;
  
    try {
        await fetch(targetUrl, { method: 'GET' });
        console.log(`Submitted URL: ${targetUrl}`);
    } catch (error) {
        console.error(`Error submitting URL: ${error}`);
    }

});
