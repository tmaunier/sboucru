var radioState = false;
  function test(button_id){
      if(radioState == false) {
          check(button_id);
          radioState = true;
      }else{
          uncheck(button_id);
          radioState = false;
      }
  }
  function check(button_id) {
      document.getElementById(button_id).checked = true;
  }
  function uncheck(button_id) {
      document.getElementById(button_id).checked = false;
  }
