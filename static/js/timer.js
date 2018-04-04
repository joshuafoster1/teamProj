
// $(document).ready(function() {

// rewite to take [{activity:***, time:***},{activity:***, time:***}]
function timerEvent(timer_intervals, initial = true){
  if (initial == true){
    var timer = new Timer();
    var currentTime = 4
    var currentActivity = 'Start in'
    var utterance = new SpeechSynthesisUtterance(currentActivity);
  } else{

    var interval = timer_intervals.shift();
    var timer = new Timer();
    var currentTime = interval["time"];
    var currentActivity = interval["activity"];
    var utterance = new SpeechSynthesisUtterance(currentActivity);
  }

    $('#timer .startButton').click(function () {
        timer.start();
    });

    $('#timer .pauseButton').click(function () {
        timer.pause();
    });

    $(timer.start({countdown: true, startValues: {seconds: currentTime}
    }));

    // if (initial == true){
    //   timer.pause();
    // };

    window.speechSynthesis.speak(utterance);
    $('#timer .current').html(currentActivity + ' ' + currentTime.toString()+' ' + 'seconds');
    if (timer_intervals[0]){
      $('#timer .next').html(timer_intervals[0]["activity"] + ' ' + timer_intervals[0]["time"].toString() + ' ' + 'seconds');
    }
    else {
      $('#timer .next').html("Finished");
    }


    timer.addEventListener('secondsUpdated', function (e) {
        $('#timer .values').html(timer.getTimeValues().toString());
    });

    timer.addEventListener('targetAchieved', function (e) {
        if(timer_intervals.length > 0){
        timerEvent(timer_intervals, initial=false);

        }
    });

};
