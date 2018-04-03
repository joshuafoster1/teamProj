
// $(document).ready(function() {

var time = [10, 25, 20, 15, 60,25, 20, 15, 60,25, 20, 15, 60,25, 20, 15, 60,25, 20, 15, 60,25, 20, 15 ];
var activity = ['Ready', 'Easy', 'Medium', 'Hard', 'Rest', 'Medium', 'Hard', 'Easy', 'Rest', 'Hard', 'Easy', 'Medium', 'Rest',
                'Easy', 'Medium', 'Hard', 'Rest', 'Medium', 'Hard', 'Easy', 'Rest', 'Hard', 'Easy', 'Medium'];

var routine = [['Ready', 3], ['Easy',25],['Medium',20], ['Hard',15]]


// rewite to take [{activity:***, time:***},{activity:***, time:***}]
function timerEvent(timer_intervals, initial = true){
    var interval = timer_intervals.shift()
    var timer = new Timer();
    var currentTime = interval["time"]
    var currentActivity = interval["activity"]
    var utterance = new SpeechSynthesisUtterance(currentActivity);

    $('#timer .startButton').click(function () {
        timer.start();
    });

    $('#timer .pauseButton').click(function () {
        timer.pause();
    });




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
        timerEvent(timer_intervals, false);

        }
    });

    $(timer.start({countdown: true, startValues: {seconds: currentTime}
    }));

    // if (initial == true){
    //   timer.pause();
    // };
};


// });
// function timerEvent2(routine, counter=0, initial = true){
//   var timer = new Timer();
//   var currentTime = routine[0][1]
//   var currentActivity = routine[0][0]
//   var utterance = new SpeechSynthesisUtterance(currentActivity);
//
//   timer.start({countdown: true, startValues: {seconds: currentTime}
//   });
//   if (initial == true){
//     timer.pause();
//   };
//   window.speechSynthesis.speak(utterance);
//
//   $('#timer .current').html(currentActivity + ' ' + currentTime.toString()+' ' + 'seconds');
//   $('#timer .next').html( currentActivity+ ' ' + currentTime.toString() + ' ' + 'seconds');
//
//   $('#timer .startButton').click(function () {
//       timer.start();
//   });
//
//   $('#timer .pauseButton').click(function () {
//       timer.pause();
//   });
//
//   timer.addEventListener('secondsUpdated', function (e) {
//       $('#timer .values').html(timer.getTimeValues().toString());
//   });
//
//   timer.addEventListener('targetAchieved', function (e) {
//       if(routine.length > 0){
//       timerEvent(routine, false);
//
//       }
//   });
//
// };
//
// // });
