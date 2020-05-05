var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'radar',
    data: {
        labels: ['DP', 'BFS', 'Brute Force', 'Binary Search', 'DFS', 'Backtracking', 'Greddy'],
        datasets: [
          {
            label: '# of Votes',
            backgroundColor: 'rgba(00, 255, 00, 0.1)',
            borderColor: 'rgba(00, 255, 00)',

            data: [12, 19, 11, 6, 8, 14, 11],
            borderWidth: 2
        }
      ]
    }
});

function getWeakPoint() {
  var i = 0;
  var min=9999;
  var name='';
  while(i<mychart.data.labels.length)
  {
    if(min >= mychart.data.datasets[i])
    {
      min = mychart.data.datasets[i];
      name = mychart.data.labels[i];
    }
    i = i+1;
  }
  document.write(name);
  document.write(min);
}

var minutesLabel = document.getElementById("minutes");
var secondsLabel = document.getElementById("seconds");
var totalSeconds = 0;

function timego() {
  setInterval(setTime, 1000);
}

function setTime() {
  ++totalSeconds;
  secondsLabel.innerHTML = pad(totalSeconds % 60);
  minutesLabel.innerHTML = pad(parseInt(totalSeconds / 60));
}

function pad(val) {
  var valString = val + "";
  if (valString.length < 2) {
    return "0" + valString;
  } else {
    return valString;
  }
}

function goBOJ() {
  var probNum = 1527;
  location.href = 'https://www.acmicpc.net/problem/' + probNum;
}
