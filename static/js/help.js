const helpPassword = document.getElementById("HelpText_password");
const helpUsername = document.getElementById("HelpText_username");

var helpViewPassword = true;
var helpViewUsername = true;

function initListener() {
	document.getElementById("helpPassword").addEventListener('click', function() {
        if (helpViewPassword) {
            helpPassword.style.display = 'block';
            helpViewPassword = false;
        } else {
            helpPassword.style.display = 'none';
            helpViewPassword = true;
		}
	});
	document.getElementById("helpUsername").addEventListener('click', function() {
        if (helpViewUsername) {
            helpUsername.style.display = 'block';
            helpViewUsername = false;
        } else {
            helpUsername.style.display = 'none';
            helpViewUsername = true;
		}
	});
};

function onLoaded(event) {
	initListener();
};

document.addEventListener('DOMContentLoaded', onLoaded);
