
// Call this function one time per second to implement a timer.
function sub1s() {

  var timenow = $('#timer').attr("value"); // use a int to store the time rest.
  var width = parseFloat(timenow) * 100 / 120; // Parse the time to a percentage.
  
  // If there's no time left, game over
  if (parseInt(timenow, 10) == 0) {
    alert('Game over!');
    window.location.assign('/survival');
  }

  // Update the timer progress bar
  $('#timer').css("width", width.toString()+"%");
  $('#timer').attr("value", (parseInt(timenow, 10)-1).toString());
  $('#time').text((parseInt(timenow, 10)).toString()+"s");

}

function calculate(a, b, ope) {

  switch (ope) {
    case "+":
      return a+b;
    case "-":
      return a-b;
    case "*":
      return a*b;
    case "/":
      return a/b;
  }

}

function getKeyboardInput(eve) {

  var keynum = window.event ? eve.keyCode : eve.which;

  /*
   * Enter:     13
   * 0-9:       48-57
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
        alert('right!');
      } else {
        alert('wrong!');
      }
      break;
    case 8:
      var num = $("#input").text();
      $("#input").text(num.substring(0, num.length - 1));
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