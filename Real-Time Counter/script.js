/*
let fruit = ['pineapple', 'orange', 'pear'];

for (let i = 0; i < fruit.length; i++) {
    console.log(fruit[i]);
}

fruit.push('mango');
fruit.unshift('green apple');
console.log(fruit);
*/

/*let student = {'vijay': 65,'ajith': 75,'rajini': 85,'kamal': 95,'MGR': 100};
function gradecheck(mark) {
    if (mark==100){
        return "A++";
    } else if (mark >= 90) {
        return "A+";
    } else if (mark >= 80) {
        return "A";
    } else if (mark >= 70) {
        return "B";
    } else if (mark >= 60) {
        return "C";
    }
}
function deptcheck(mark) {
    if (mark==100){
        return "Agriculture";
    } else if (mark >= 90) {
        return "Viscom";
    } else if (mark >= 80) {
        return "Computer Science";
    } else if (mark >= 70) {
        return "Electronics";
    } else if (mark >= 60) {
        return "Politics";
    }
}

for (let name in student) {
    console.log('Name:', name,' _ Mark:', student[name],' _ Grade:', gradecheck(student[name]),' _ Dept:', deptcheck(student[name]));
}
*/

const textcontent = document.getElementById("textInput");
const remainingChars= document.getElementById("right");
const totalChars = document.getElementById("left");

textcontent.addEventListener('input',() =>{
            const length = textcontent.value.length;
            remainingChars.textContent=50-length;
            totalChars.textContent= length;
});

