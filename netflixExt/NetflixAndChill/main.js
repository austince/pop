// What is injected into 

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    /*if( request.message === "clicked_browser_action" ) {
      chrome.runtime.sendMessage({"message": "started_movie", "movie": "child"});
    }*/
  }
);