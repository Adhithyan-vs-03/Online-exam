// Menu Icon Click Event

const Menu = document.getElementById('menu');
const Hidden = document.getElementById('hidden');
const html = document.getElementById('html')

Menu.addEventListener('click',()=>{
    if (Hidden.style.display==='block'){ Hidden.style.display='none';}
    else{Hidden.style.display='block'}
});
// html.addEventListener('click',()=>{
//     if (Hidden.style.display==='block'){ Hidden.style.display='none';}
// });


//About Click Event

const openPopup = document.querySelector('.popup-btn')
const closePopup = document.querySelector('.close-popup')
const Overlay = document.querySelector('.overlay')

openPopup.addEventListener('click',()=>{
        Overlay.style.display='flex';
});
closePopup.addEventListener('click',()=>{
    Overlay.style.display='none';
});
Overlay.addEventListener('click',(e)=>{
    if(e.target===Overlay){Overlay.style.display='none';}
});

//Gallery View

let images =[
    {src:"/static/gallery/entrance.jpg",
        title:"Entrance Exams: To evaluate students' eligibility for various courses."},
    {src:"/static/gallery/semester.jpg",
        title:"Semester Exams: Online assessments replacing traditional pen-paper exams for courses and degrees."},
    {src:"/static/gallery/mock.jpg",
        title:"Online Mock Exams: Institutes conduct mock exams to prepare students for final or competitive exams."},
    {src:"/static/gallery/diagnostic.jpg",
        title:"Competitive Exams: Exams conducted for national-level recruitment or competitive eligibility"},
    {src:"/static/gallery/english.jpg",
        title:"Skill-Based Exams: Online exams to evaluate skill mastery in programming, design, or other areas"}   
]
let currentIndex =0

function showImage(){
    const imgElement = document.getElementById("image1");
    const details = document.getElementById('img-detail');
    imgElement.src =images[currentIndex].src;
    details.innerText = images[currentIndex].title;
}
function nextImage(){
    currentIndex=(currentIndex + 1) % images.length;
    showImage();
}
function previewImage(){
    currentIndex=(currentIndex - 1 + images.length) % images.length;
    showImage();
}
showImage();
