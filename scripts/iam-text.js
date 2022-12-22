const iams = ['maker', 'environment lead', 'probably planning an event', 'working on a blog', 'former apprentice'];
var pointer = 0
setInterval(function() {
    document.getElementById('iam-text').innerHTML=`I am an IT consultant and ${iams[pointer]}.`;
    pointer++;
    if (pointer > iams.length - 1) {
        pointer = 0;
    }
  }, 5000);