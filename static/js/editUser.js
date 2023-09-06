var password_change = false;
      document.getElementById("password").addEventListener("input", function() {
        if (document.getElementById("password").value != "") {
          document.getElementById("new_password").disabled = false;
          document.getElementById("password_confirm").disabled = false;
          password_change = true;
          if (document.getElementById("new_password").value == "" && document.getElementById("password_confirm").value== "") {
            document.getElementById("data_submit").disabled = true;
          } else {
            document.getElementById("data_submit").disabled = false;
          }
          
        } else {
          document.getElementById("new_password").disabled = true;
          document.getElementById("password_confirm").disabled = true;
          password_change = false;
        }
      });
        document.getElementById("new_password").addEventListener("input", function() {
          if (document.getElementById("new_password").value != document.getElementById("password_confirm").value && password_change) {
            document.getElementById("data_submit").disabled = true;
          } else {
            document.getElementById("data_submit").disabled = false;
          }
        });
        document.getElementById("password_confirm").addEventListener("input", function() {
          if (document.getElementById("new_password").value != document.getElementById("password_confirm").value && password_change) {
            document.getElementById("data_submit").disabled = true;
          } else {
            document.getElementById("data_submit").disabled = false;
          }
        });