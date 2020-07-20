
let user_points = sessionStorage.getItem("points");
let user_time = sessionStorage.getItem("time");

console.log(user_time,user_points)
document.querySelector(".points").innerHTML = user_points;
document.querySelector("#time_taken").innerHTML = user_time;

