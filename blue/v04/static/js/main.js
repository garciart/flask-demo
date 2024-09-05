// code: language=javascript
// Set copyright ending year to current year
let date = new Date();
let fullYear = date.getFullYear();
document.getElementById("currentYear").innerHTML = (fullYear !== 2023 ? "2023 -" : "") + fullYear;
