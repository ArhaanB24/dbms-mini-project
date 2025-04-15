const openpopup = document.querySelectorAll("[data-profile-target]")
const closepopup = document.querySelectorAll("[data-close-button]")
const overlay = document.getElementById("overlay")
const openpdf = document.querySelectorAll("[data-preview-target]")
const openotp = document.querySelectorAll("[data-otp-target]")
var previews = document.querySelectorAll("#preview")
const addsubjects = document.querySelectorAll("[data-addsub-target]")
const closeaddsub = document.querySelectorAll("[data-close-button]")
const closepdf = document.querySelectorAll("[data-closepdf-button]")
const remsubjects = document.querySelectorAll("[data-remsub-target]")
const closeremsub = document.querySelectorAll("[data-close-button]")
const uploadfile = document.querySelectorAll("[data-upload-target]")
const closeuploadfile = document.querySelectorAll("[data-close-button]")
const closeotp = document.querySelectorAll("[data-close-button]")
var count = 0
//finish javascript copy paste add subjects

function copytext(text){
    console.log("Clicked")
    navigator.clipboard.writeText(text)
    alert("Link copied to clipboard")
}
previews.forEach(preview => {
    preview.addEventListener("click",() => {
        previewstring = preview.value
        previewstringnew = previewstring.replace(/'/g, '"')
        const previewobj = JSON.parse(previewstringnew)
        console.log(previewobj)
        src = `${previewobj["filelink"]}`
        desc = `${previewobj["description"]}`
        upby = `${previewobj["uploaded_by"]}`
        pdflink = `${previewobj["filelink"]}`
        filename = `${previewobj["filename"]}`
        console.log(filename)
        document.getElementById("preview-pdf").innerHTML = `
        <iframe id="preview-pdf-file" src="${src}"></iframe>
        <div class="h-1/2 w-1/2 flex justify-center items-center flex-col mt-[10rem]" id="descbox">
        <div class="desc w-3/4 bg-[#FFFFFF] rounded-xl p-[3rem]">
        <p class="font-bold text-xl size-10">Description</p>
        <p class="h-28 overflow-y-scroll">${desc}</p>
        <p class="w-full font-bold text-xl size-10">Uploaded By</p>
        <p class="mb-6">${upby}</p>
        <div class="w-full flex justify-center">
            <button class="w-full bg-[#583DA1] text-[#EFEFEF] rounded-full p-4" type="button" onclick="copytext('https://www.notesportal.tech/${filename}')">Copy Link</button>
        </div>
        </div>
        <a href="https://www.instagram.com/neurotechh/" target="_blank">
        <img src="/static/notesportalAd.svg" class="mt-[2rem] w-[13rem] h-[13rem]">
        </a>
        <div>
        `     
    })
})
openpopup.forEach(button => {
    button.addEventListener("click",() => {
        const popup = document.querySelector(button.dataset.profileTarget)
        console.log(button.dataset)
        openpopupfunc(popup)
        console.log("Hello World")
    })
})
openotp.forEach(button => {
    button.addEventListener("click",() => {
        console.log(button.dataset)
        const otppopup = document.querySelector(button.dataset.otpTarget)
        console.log("Hello World")
        openpopupfunc(otppopup)
    })
})
addsubjects.forEach(button => {
    button.addEventListener("click",() => {
        console.log(button.dataset)
        const addsubpopup = document.querySelector(button.dataset.addsubTarget)
        openpopupfunc(addsubpopup)
        console.log("Hello World")
    })
})  
remsubjects.forEach(button => {
    button.addEventListener("click",() => {
        console.log(button.dataset)
        const remsubpopup = document.querySelector(button.dataset.remsubTarget)
        openpopupfunc(remsubpopup)
        console.log("Hello World")
    })
}) 
uploadfile.forEach( button => {
    button.addEventListener('click',() => {
        const uploadpopup = document.querySelector(button.dataset.uploadTarget)
        openpopupfunc(uploadpopup)
    })
})
openpdf.forEach(button => {
    button.addEventListener("click",() => {
        const pdf = document.querySelector(button.dataset.previewTarget)
        console.log(button.dataset)
        openpopupfunc(pdf)
        console.log("Hello World")
    })
})

closepdf.forEach(button => {
    button.addEventListener("click",() => {
        const pdf = button.closest(".preview-pdf")
        document.getElementById("preview-pdf").innerHTML = ""
        closepopupfunc(pdf)
    })
})
closepopup.forEach(button => {
    button.addEventListener("click",() => {
        const popup = button.closest(".profile-open")
        closepopupfunc(popup)
    })
})
closeotp.forEach(button => {
    button.addEventListener("click",() => {
        const popup = button.closest(".otppop")
        closepopupfunc(popup)
    })
})
closeaddsub.forEach(button => {
    button.addEventListener("click",() => {
        const popup = button.closest(".addsub")
        popup.classList.remove("active")
        overlay.classList.remove("active")
    })
})
closeremsub.forEach(button => {
    button.addEventListener("click",() => {
        const popup = button.closest(".remsub")
        popup.classList.remove("active")
        overlay.classList.remove("active")
    })
})
closeuploadfile.forEach(button => {
    button.addEventListener("click",() => {
        const popup = button.closest(".uploadfile")
        popup.classList.remove("active")
        overlay.classList.remove("active")
    })
})
overlay.addEventListener('click', () => {
    const popups = document.querySelectorAll('.profile-open.active')
    const pdfs = document.querySelectorAll(".preview-pdf.active")
    document.getElementById("preview-pdf").innerHTML = ""
    popups.forEach(popup => {
      closepopupfunc(popup)
      
    })
    pdfs.forEach(pdf => {
        closepopupfunc(pdf)
    })
  })

function openpopupfunc(popup)
{
    if (popup == null ) return
    popup.classList.add("active")
    overlay.classList.add("active")
    
}
function closepopupfunc(popup)
{
    if (popup == null) 
    return
    popup.classList.remove("active")
    overlay.classList.remove("active")
}
function easteregg(){
    if (count < 7)
    {
        count += 1;
        console.log(count)
    }
    else{
        count = 0;
        window.open("/sharvil")
    }
}

