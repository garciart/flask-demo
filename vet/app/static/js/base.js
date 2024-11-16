// Set copyright ending year to current year
let date = new Date();
let fullYear = date.getFullYear();
document.getElementById("currentYear").innerHTML = (fullYear !== 2024 ? "2024 -" : "") + fullYear;
