document.getElementById("password").addEventListener("input", function (e) {
  var password = e.target.value;
  var criteria = [
    {
      test: (pwd) => pwd.length > 7,
      message: "Mindestens 8 Zeichen lang",
      weight: 2,
    },
    {
      test: (pwd) => /[a-z]/.test(pwd),
      message: "Mindestens ein Kleinbuchstabe",
      weight: 1,
    },
    {
      test: (pwd) => /[A-Z]/.test(pwd),
      message: "Mindestens ein Großbuchstabe",
      weight: 1,
    },
    {
      test: (pwd) => /[0-9]/.test(pwd),
      message: "Mindestens eine Ziffer",
      weight: 1,
    },
    {
      test: (pwd) => /[\W_]/.test(pwd),
      message: "Mindestens ein Sonderzeichen",
      weight: 1,
    },
    {
      test: (pwd) => !containsSequentialNumbers(pwd),
      message: "Keine aufeinanderfolgenden Zahlen erlaubt",
      weight: 3,
    },
  ];

  var strengthBar = document.getElementById("passwordStrength");
  var feedbackList = document.getElementById("passwordFeedback");
  feedbackList.innerHTML = ""; // Clear previous feedback
  var totalWeight = criteria.reduce(
    (acc, criterion) => acc + criterion.weight,
    0
  );
  var strength = 0;

  criteria.forEach((criterion) => {
    if (criterion.test(password)) {
      strength += criterion.weight;
    } else {
      var li = document.createElement("li");
      li.textContent = criterion.message;
      feedbackList.appendChild(li);
    }
  });

  var strengthPercentage = strength / totalWeight;
  var strengthText = getStrengthText(strengthPercentage);
  strengthBar.textContent = "Passwortstärke: " + strengthText;
  strengthBar.style.display = "block";
});

function containsSequentialNumbers(password) {
  for (let i = 0; i < password.length - 2; i++) {
    if (
      parseInt(password[i]) + 1 === parseInt(password[i + 1]) &&
      parseInt(password[i + 1]) + 1 === parseInt(password[i + 2])
    ) {
      return true;
    }
  }
  return false;
}

function getStrengthText(percentage) {
  if (percentage < 0.4) return "Sehr schwach";
  if (percentage < 0.6) return "Schwach";
  if (percentage < 0.8) return "Mittel";
  if (percentage < 1) return "Stark";
  return "Sehr stark";
}
