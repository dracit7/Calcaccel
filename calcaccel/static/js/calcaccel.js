
/* Global vars */

var swalswitch = 1;

/*
 * Helper functions
 */

function getTime() {
  return parseInt($('#timer').attr("value"), 10);
}

function getScore() {
  return parseInt($('#score').text(), 10);
}

function getRank() {
  if (getScore() < 30) {
    return 1;
  } else if (getScore() < 80) {
    return 2;
  } else if (getScore() < 150) {
    return 3
  } else {
    return 4;
  }
}

function deleteMistake(content) {

  var req = new XMLHttpRequest();
  req.open('POST', '/home/mistakes/delete');

  req.send("content=" + content);

}

/*
 * Survival mode (some are global) functions
 */

// Call this function one time per second to implement a timer.
// Or, call it to punish someone.
function sub1s() {

  var timenow = $('#timer').attr("value"); // use a int to store the time rest.
  var width = parseFloat(timenow) * 100 / 120; // Parse the time to a percentage.

  const Toast = Swal.mixin({
    showConfirmButton: true,
    animation: true,
    allowOutsideClick: false,
    allowEscapeKey: false,
    allowEnterKey: false,
  });

  // If there's no time left, game over
  if (parseInt(timenow, 10) <= 0) {
    if (swalswitch == 1) {

      var scorePost = new XMLHttpRequest();
      var form = new FormData();
      if (scorePost == null) {
        alert('Your browser does not support XMLHttpRequest, please update your browser.');
      } else {
        scorePost.open("POST", "/survival/score");
        form.append("score", getScore())
        scorePost.send(form);
      }

      Toast.fire({
        type: "info",
        titleText: "Game over!",
        html: "<p>Your Total score is <span class='score'>" + $('#score').text() + "</span> !</p>",
        confirmButtonText: "View scoreboard",
        preConfirm: () => {
          return window.location.replace("/survival/scoreboard");
        },
      });
    }
    swalswitch = 0;
  }

  // Update the timer progress bar
  $('#timer').css("width", width.toString() + "%");
  $('#timer').attr("value", (parseInt(timenow, 10) - 1).toString());
  $('#time').text((parseInt(timenow, 10)).toString() + "s");

  checkprogress();
  $('#level').text(getRank());

  $('#time-control').text("");

}

function sub1sSafe() {

  var timenow = $('#timer').attr("value"); // use a int to store the time rest.
  var width = parseFloat(timenow) * 100 / 120; // Parse the time to a percentage.

  // Update the timer progress bar
  $('#timer').css("width", width.toString() + "%");
  $('#timer').attr("value", (parseInt(timenow, 10) - 1).toString());
  $('#time').text((parseInt(timenow, 10)).toString() + "s");

  checkprogress();

  $('#time-control').text("");

}

// Call this function to increase the value of timer by x.
function plusxs(x) {

  var timenow = $('#timer').attr("value"); // use a int to store the time rest.
  var width = parseFloat(timenow) * 100 / 120; // Parse the time to a percentage.

  // Update the timer progress bar
  $('#timer').css("width", width.toString() + "%");
  $('#timer').attr("value", (parseInt(timenow, 10) + x).toString());
  $('#time').text((parseInt(timenow, 10)).toString() + "s");

  checkprogress();

  $('#time-control').text("+" + x.toString() + "s");

}

// If time left exceeds 120s, then change the outfit of the progress bar.
function checkprogress() {

  var timenow = $('#timer').attr("value"); // use a int to store the time rest.

  if (parseInt(timenow, 10) < 10) {

    if ($('#timer').hasClass('bg-success')) {
      $('#timer').removeClass('bg-success');
      $('#timer').addClass('bg-danger');
    } else if ($('#timer').hasClass('bg-info')) {
      $('#timer').removeClass('bg-info');
      $('#timer').addClass('bg-danger');
    } else if ($('#timer').hasClass('bg-primary')) {
      $('#timer').removeClass('bg-primary');
      $('#timer').addClass('bg-danger');
    }

    $('#time').css("font-size", "180%");

  } else if (parseInt(timenow, 10) < 60) {

    if ($('#timer').hasClass('bg-danger')) {
      $('#timer').removeClass('bg-danger');
      $('#timer').addClass('bg-success');
    } else if ($('#timer').hasClass('bg-info')) {
      $('#timer').removeClass('bg-info');
      $('#timer').addClass('bg-success');
    } else if ($('#timer').hasClass('bg-primary')) {
      $('#timer').removeClass('bg-primary');
      $('#timer').addClass('bg-success');
    }

    $('#time').css("font-size", "180%");

  } else if (parseInt(timenow, 10) < 120) {

    if ($('#timer').hasClass('bg-danger')) {
      $('#timer').removeClass('bg-danger');
      $('#timer').addClass('bg-info');
    } else if ($('#timer').hasClass('bg-success')) {
      $('#timer').removeClass('bg-success');
      $('#timer').addClass('bg-info');
    } else if ($('#timer').hasClass('bg-primary')) {
      $('#timer').removeClass('bg-primary');
      $('#timer').addClass('bg-info');
    }

    $('#time').css("font-size", "180%");

  } else {

    if ($('#timer').hasClass('bg-danger')) {
      $('#timer').removeClass('bg-danger');
      $('#timer').addClass('bg-primary');
    } else if ($('#timer').hasClass('bg-success')) {
      $('#timer').removeClass('bg-success');
      $('#timer').addClass('bg-primary');
    } else if ($('#timer').hasClass('bg-info')) {
      $('#timer').removeClass('bg-info');
      $('#timer').addClass('bg-primary');
    }

    $('#time').css("font-size", "300%");

  }

}

// return a ope b
function calculate(a, b, ope) {

  switch (ope) {
    case "+":
      return a + b;
    case "-":
      return a - b;
    case "*":
      return a * b;
    case "/":
      return a / b;
  }

}

// Rank 1:
//   +-*/, 0 < operand <= 10, add 5s per correction, sub 1s per fault
// Rank 2:
//   +-*/, -10 < operand <= 10, add 5s per correction, sub 2s per fault
// Rank 3:
//   +-*/, -10 < operand <= 10, add 3s per correction, sub 3s per fault
// Rank 4:
//   +-*/, -20 < operand <= 20, add 3s per correction, sub 4s per fault
function init_quiz(rank) {

  var ope_l;
  var ope_r;
  var ope;

  switch (rank) {
    case 1:
      ope_l = Math.floor(Math.random() * 10);
      ope_r = Math.floor(Math.random() * ope_l);
      switch (Math.floor(Math.random() * 4)) {
        case 0:
          ope = '+';
          break;
        case 1:
          ope = '-';
          break;
        case 2:
          ope = '*';
          break;
        case 3:
          ope = '/';
          if (ope_r == 0) ope_r += 1;
          ope_l = Math.floor(Math.random() * 10 + 1) * ope_r;
          break;
      }
      $('#operand-l').text(ope_l.toString());
      $('#operand-r').text(ope_r.toString());
      $('#operator').text(ope);
      break;
    case 2:
    case 3:
      ope_l = Math.floor(Math.random() * 20) - 10;
      ope_r = Math.floor(Math.random() * 20) - 10;
      if (ope_r == 0) {
        ope_r++;
      }
      switch (Math.floor(Math.random() * 4)) {
        case 0:
          ope = '+';
          break;
        case 1:
          ope = '-';
          break;
        case 2:
          ope = '*';
          break;
        case 3:
          ope = '/';
          ope_l = Math.floor(Math.random() * 10 + 1) * ope_r;
          break;
      }
      $('#operand-l').text(ope_l.toString());
      $('#operand-r').text(ope_r.toString());
      $('#operator').text(ope);
      break;
    case 4:
      ope_l = Math.floor(Math.random() * 40) - 20;
      ope_r = Math.floor(Math.random() * 40) - 20;
      switch (Math.floor(Math.random() * 4)) {
        case 0:
          ope = '+';
          break;
        case 1:
          ope = '-';
          break;
        case 2:
          ope = '*';
          break;
        case 3:
          ope = '/';
          ope_l = Math.floor(Math.random() * 20 - 10) * ope_r;
          if (ope_l == 0) {
            ope_l = -1;
          }
          break;
      }
      $('#operand-l').text(ope_l.toString());
      $('#operand-r').text(ope_r.toString());
      $('#operator').text(ope);
      break;

  }

  $('#operand-l').text()

}

// Increase the score by `credit` times.
function incscore(credit) {

  var score = getScore();

  // If we're in ACCEL TIME, double the credit.
  if (getTime() > 120) {
    $('#score').text((score + 2 * credit).toString());
  } else {
    $('#score').text((score + credit).toString());
  }

  // Animation
  anime.timeline()
    .add({
      targets: '#score',
      opacity: [0, 1],
      fontSize: ['150%', '100%'],
      easing: "easeInOutCirc",
      duration: 500,
      delay: 0,
    });

}

// Catch a keyboard input a handle it.
function getKeyboardInput(eve) {

  var keynum = window.event ? eve.keyCode : eve.which;

  /*
   * Enter:     13
   * 0-9:       48-57
   * -:         189
   * Backspace: 8
   */
  switch (keynum) {
    case 13:
      var result = calculate(
        parseInt($('#operand-l').text(), 10),
        parseInt($('#operand-r').text(), 10),
        $('#operator').text()
      );
      if (result == parseInt($('#input').text(), 10)) {

        // If answered right, increase time 
        switch (getRank()) {
          case 1: case 2:
            plusxs(5);
            break;
          case 3: case 4:
            plusxs(3);
            break;
        }

        // Clear input buffer
        $("#input").text("");

        // Score
        incscore(1);

      } else {

        // Elsewise, decrease time
        for (let i = 0; i < getRank(); i++) {
          sub1sSafe();
        }
        $("#input").text("");
        $('#time-control').text("-" + getRank().toString() + "s");

        recordMistake();

      }

      init_quiz(getRank());

      break;

    case 8:
      var num = $("#input").text();
      $("#input").text(num.substring(0, num.length - 1));
      break;
    case 189:
      $('#input').text($('#input').text() + "-");
      break;
    case 48:
      $('#input').text($('#input').text() + "0");
      break;
    case 49:
      $('#input').text($('#input').text() + "1");
      break;
    case 50:
      $('#input').text($('#input').text() + "2");
      break;
    case 51:
      $('#input').text($('#input').text() + "3");
      break;
    case 52:
      $('#input').text($('#input').text() + "4");
      break;
    case 53:
      $('#input').text($('#input').text() + "5");
      break;
    case 54:
      $('#input').text($('#input').text() + "6");
      break;
    case 55:
      $('#input').text($('#input').text() + "7");
      break;
    case 56:
      $('#input').text($('#input').text() + "8");
      break;
    case 57:
      $('#input').text($('#input').text() + "9");
      break;
  }

}

/*
 * Dual mode functions
 */

// Get peer's state from /dual/message
function getPeerState() {

  var req = new XMLHttpRequest();
  if (req == null) {
    alert('Your browser does not support XMLHttpRequest, please update your browser.');
    return -1;
  }

  req.onreadystatechange = function () {
    if (req.responseText != "") {

      var form = JSON.parse(req.responseText);
      var width = parseFloat(form.timeleft) * 100 / 120;

      if (form.score == -1) {
        form.score = $('#peer-score').text();
      }

      $('#peer-time').text(form.timeleft + "s");
      $('#peer-timer').css("width", width.toString() + "%");
      $('#peer-timer').attr("value", form.timeleft);
      $('#peer-score').text(form.score);

      if (form.timeleft < 0 && getTime() < 0) {
        if (getScore() > form.score)
          settlement("win");
        else if (getScore() == form.score)
          settlement("draw");
        else
          settlement("lose");
      } else if (form.timeleft < 0 && getTime() > 0) {
        if (getScore() > form.score) {
          settlement("win");
        }
      } else if (form.timeleft > 0 && getTime() < 0) {
        if (getScore() < form.score) {
          settlement("lose");
        }
      }

    }
  }

  req.open('GET', '/dual/message');
  req.send();

}

// Send state to peer and sub1s
function sendState() {

  var timenow = $('#timer').attr("value"); // use a int to store the time rest.
  var width = parseFloat(timenow) * 100 / 120; // Parse the time to a percentage.

  // Update the timer progress bar
  $('#timer').css("width", width.toString() + "%");
  $('#timer').attr("value", (parseInt(timenow, 10) - 1).toString());
  $('#time').text((parseInt(timenow, 10)).toString() + "s");

  checkprogress();

  $('#time-control').text("");

  var req = new XMLHttpRequest();
  var form = new FormData();
  if (req == null) {
    alert('Your browser does not support XMLHttpRequest, please update your browser.');
    return -1;
  }

  form.append("score", getScore());
  form.append("timeleft", getTime());
  req.open("POST", "/dual/message");
  req.send(form);

}

function settlement(result) {

  clearInterval(sendHandler);
  clearInterval(getHandler);

  const Toast = Swal.mixin({
    showConfirmButton: true,
    animation: true,
    allowOutsideClick: false,
    allowEscapeKey: false,
    allowEnterKey: false,
  });

  var request = new XMLHttpRequest();
  request.open("POST", "/dual/settlement");
  request.send(null)

  if (result == "win") {
    Toast.fire({
      type: "success",
      title: "You win!",
      html: "<p>Your score: <span class='score'>" + $('#score').text() + "</span></p> \
      <p>Opponent's score: <span class='score'>" + $('#peer-score').text() + "</span></p>",
      confirmButtonText: "Main menu",
      preConfirm: () => {
        return window.location.replace("/dual");
      },
    })
  } else if (result == "lose") {
    Toast.fire({
      type: "error",
      title: "You lose!",
      html: "<p>Your score: <span class='score'>" + $('#score').text() + "</span></p> \
      <p>Opponent's score: <span class='score'>" + $('#peer-score').text() + "</span></p>",
      confirmButtonText: "Main menu",
      preConfirm: () => {
        return window.location.replace("/dual");
      },

    })
  } else {
    Toast.fire({
      type: "info",
      title: "Draw.",
      html: "<p>Your score: <span class='score'>" + $('#score').text() + "</span></p> \
      <p>Opponent's score: <span class='score'>" + $('#peer-score').text() + "</span></p>",
      confirmButtonText: "Main menu",
      preConfirm: () => {
        return window.location.replace("/dual");
      },
    })

  }

}

function recordMistake() {

  var req = new XMLHttpRequest();
  req.open("POST", "/home/mistakes");

  var form = new FormData();
  form.append(
    "mistake",
    $('#operand-l').text() + $('#operator').text() + $('#operand-r').text()
  );

  req.send(form);

}