// Create the toastParent element if it doesn't exist
let toastParent = document.getElementById("toast_parent-TurboLancer");
let activeToasts = [];

function toast(type, text, padding = 0) {
  console.log("triggered...");

  // Create the toastParent if it doesn't exist
  if (!toastParent) {
    toastParent = document.createElement("div");
    toastParent.id = "toast_parent-TurboLancer";
    document.body.appendChild(toastParent);
  }

  const toastElement = document.createElement("div");
  toastElement.classList.add("toast-TurboLancer");
  toastElement.setAttribute("role", "alert");
  toastElement.id = type;

  const toastContent = document.createElement("div");
  toastContent.classList.add("toast-contentt");
  toastElement.appendChild(toastContent);

  const toastIcon = document.createElement("div");
  toastIcon.classList.add("toast-icont");
  toastContent.appendChild(toastIcon);

  const icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  icon.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  icon.setAttribute("width", "16");
  icon.setAttribute("height", "16");
  icon.setAttribute("fill", "currentColor");
  icon.setAttribute("viewBox", "0 0 16 16");
  toastIcon.appendChild(icon);

  const iconPath = document.createElementNS(
    "http://www.w3.org/2000/svg",
    "path"
  );
  if (type === "s") {
    iconPath.setAttribute(
      "d",
      "M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"
    );
  } else if (type === "d") {
    iconPath.setAttribute(
      "d",
      "M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"
    );
  } else if (type === "w") {
    iconPath.setAttribute(
      "d",
      "M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"
    );
  }
  icon.appendChild(iconPath);

  const toastText = document.createElement("div");
  toastText.classList.add("toasttextt");
  toastContent.appendChild(toastText);

  const textNode = document.createElement("p");
  textNode.textContent = text;
  textNode.style.paddingTop = `${padding}px`;
  toastText.appendChild(textNode);

  toastParent.appendChild(toastElement);

  const toastTimeout = setTimeout(() => {
    toastElement.classList.add("go");
    setTimeout(() => {
      toastElement.classList.remove("go");
      toastElement.classList.add("none");
      toastParent.removeChild(toastElement);
      activeToasts = activeToasts.filter((t) => t.element !== toastElement);

      // Remove the toastParent if it's empty
      if (!toastParent.hasChildNodes()) {
        document.body.removeChild(toastParent);
        toastParent = null;
      }
    }, 400);
  }, 4000); // Display the toast for 4 seconds

  activeToasts.push({ element: toastElement, timeout: toastTimeout });
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function openit(x) {
  x.onload = () =>{
    console.log('opened')
  }
  const div = document.createElement("div");
  div.id = "imgvp";
  document.body.appendChild(div);
  const img = x.cloneNode(true);
  img.id = "";
  img.className = "";
  img.onclick = null;

  img.style.width = "auto";
  img.style.maxWidth = "800px";
  img.style.maxHeight = "80%";
  img.style.borderRadius = "10px";
  img.style.animation = "showupimg 0.4s ease";
  div.appendChild(img);
  div.addEventListener("click", function () {
    this.classList.add("go");
    setTimeout(() => {
      this.remove();
    }, 400);
  });
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
window.addEventListener("DOMContentLoaded", function () {
  function deleteCookie(cookieName) {
    try {
      const expirationDate = new Date(0);
      const formattedDate = expirationDate.toUTCString();
      document.cookie = `${cookieName}=; expires=${formattedDate}; path=/;`;
    } catch (error) {
      console.error(`Error deleting cookie "${cookieName}":`, error);
    }
  }

  function deleteCookiesAndReload(cookieNames) {
    try {
      cookieNames.forEach(deleteCookie);
      window.location.reload();
    } catch (error) {
      console.error("Error deleting cookies and reloading page:", error);
    }
  }
  const deleteButtons = document.querySelectorAll("#LogOutButton");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const cookiesToDelete = ["ideo", "emalo", "deno", "tp"];
      deleteCookiesAndReload(cookiesToDelete);
    });
  });
});
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
function getMonthsArray(startMonthYear) {
  const start_date = new Date(startMonthYear);
  const current_date = new Date();
  const months_array = [];

  for (
    let year = start_date.getFullYear();
    year <= current_date.getFullYear();
    year++
  ) {
    const endMonth =
      year === current_date.getFullYear() ? current_date.getMonth() : 11;
    for (
      let month = year === start_date.getFullYear() ? start_date.getMonth() : 0;
      month <= endMonth;
      month++
    ) {
      const date_obj = new Date(year, month, 1);
      months_array.push(
        date_obj.toLocaleString("en-US", { year: "numeric", month: "short" })
      );
    }
  }
  console.log(months_array);
  return months_array;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
function modal(type, modalText, buttonText, buttonId, data_to_taransfor = "",cncle = 'Close',cid = '') {
  // Create the modal container
  const modal = document.createElement("div");
  modal.classList.add("Modal_GLOBAL");
  // Create the modal content
  const modalContentM = document.createElement("div");
  modalContentM.classList.add("Modal_GLOBAL-content");
  modalContentM.style.padding = '20px'

  // Create the modal body
  const modalBody = document.createElement("div");
  modalBody.classList.add("Modal_GLOBAL-body");

  // Create the icon
  let icon;
  switch (type) {
    case "i":
      icon = `<svg class = "info-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM216 336h24V272H216c-13.3 0-24-10.7-24-24s10.7-24 24-24h48c13.3 0 24 10.7 24 24v88h8c13.3 0 24 10.7 24 24s-10.7 24-24 24H216c-13.3 0-24-10.7-24-24s10.7-24 24-24zm40-208a32 32 0 1 1 0 64 32 32 0 1 1 0-64z"/></svg>`;
      break;
    case "s":
      icon = `<svg class = "success-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M256 48a208 208 0 1 1 0 416 208 208 0 1 1 0-416zm0 464A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209c9.4-9.4 9.4-24.6 0-33.9s-24.6-9.4-33.9 0l-111 111-47-47c-9.4-9.4-24.6-9.4-33.9 0s-9.4 24.6 0 33.9l64 64c9.4 9.4 24.6 9.4 33.9 0L369 209z"/></svg>`;
      break;
    case "w":
      icon = `<svg class = "warning-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z"/></svg>`;
      break;
    case "d":
      icon = `<svg class=" danger-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
        </svg>`;
      break;
  }

  const textNode = document.createTextNode(modalText);

  modalBody.innerHTML = icon;
  modalBody.appendChild(textNode);

  const modalFooter = document.createElement("div");
  modalFooter.classList.add("Modal_GLOBAL-footer");

  const actionButton = document.createElement("button");
  actionButton.onclick = () => {
    closeModalM(modal, modalContentM);
  };
  actionButton.classList.add("Mbtn", type);
  actionButton.setAttribute("id", buttonId);
  actionButton.textContent = buttonText;

  actionButton.setAttribute("data-given", data_to_taransfor);

  const closeButton = document.createElement("button");
  closeButton.classList.add("closeMX");
  closeButton.innerHTML = "&times;";
  closeButton.onclick = () => {
    closeModalM(modal, modalContentM);
  };

  const closeModalButton = document.createElement("button");
  closeModalButton.classList.add("Mbtn", "Mcancle");
  closeModalButton.textContent = cncle;
  closeModalButton.id = cid
  closeModalButton.onclick = () => {
    closeModalM(modal, modalContentM);
  };

  modalFooter.appendChild(actionButton);
  modalFooter.appendChild(closeModalButton);
  modalBody.appendChild(closeButton);

  modalContentM.appendChild(modalBody);
  modalContentM.appendChild(modalFooter);

  modal.appendChild(modalContentM);

  document.body.appendChild(modal);

  openModalM(modal, modalContentM);
}

function openModalM(modal, modalContentM) {
  modal.classList.add("open");
  modalContentM.classList.add("open");
  modal.style.display = "flex";
}

function closeModalM(modal, modalContentM) {
  modalContentM.classList.add("close");
  modalContentM.addEventListener(
    "animationend",
    function () {
      modalContentM.classList.remove("close", "open");
      modal.classList.remove("open");

      modal.remove();
    },
    { once: true }
  );
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
function details(url, other = false) {
  const modal = document.createElement("div");
  modal.classList.add("Modal_GLOBAL", "D");

  const modalContent = document.createElement("div");
  modalContent.classList.add("Modal_GLOBAL-content", "D");
  modalContent.style.width = "92svw";
  modalContent.style.height = "92svh";
  const iframe = document.createElement("iframe");
  if(!other){
      iframe.src = "/full_catalogue/" + url;

  }
  else if (other){
    iframe.src =  url;

  }
  iframe.style.width = "100%";
  iframe.style.height = "94%";
  iframe.style.borderRadius = '10px'

  const closeButton = document.createElement("button");
  closeButton.classList.add("closeMX");
  closeButton.innerHTML = "&times;";
  closeButton.style.fontSize = "22px";
  closeButton.onclick = function () {
    closeModal()
  };
  modal.onclick = function () {
    closeModal()
  };
  modalContent.appendChild(iframe);
  modalContent.appendChild(closeButton);

  modal.appendChild(modalContent);

  document.body.appendChild(modal);

  openModal(modal, modalContent);
}

function openModal(modal, modalContent) {
  modal.classList.add("open");
  modalContent.classList.add("open");
  modal.style.display = "flex";
}

function closeModal() {
  const modal = document.querySelector(".Modal_GLOBAL.open");
  const modalContent = document.querySelector(".Modal_GLOBAL-content.open");

  if (modal && modalContent) {
    modalContent.classList.add("close");
    modalContent.addEventListener(
      "animationend",
      function () {
        modalContent.classList.remove("close", "open");
        modal.classList.remove("open");
        modal.remove();
      },
      { once: true }
    );
  }
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
function addIframeOverlay() {
  const iframes = document.querySelectorAll("iframe");

  iframes.forEach((iframe) => {
    if (
      iframe.parentNode.querySelector(".iframe-overlay") ||
      iframe.hasAttribute("data-overlay-added")
    ) {
      return;
    }

    const icon = document.createElement("span");
    icon.classList.add("iframe-icon");
    icon.style.position = "absolute";
    icon.style.bottom = "20px";
    icon.style.right = "25px";
    icon.style.width = "30px";
    icon.style.height = "30px";
    icon.style.borderRadius = "50%";
    icon.style.backgroundColor = "#0000008a";
    icon.style.display = "flex";
    icon.style.flexDirection = "row";
    icon.style.justifyContent = "center";
    icon.style.alignItems = "center";
    icon.style.cursor = "pointer";
    icon.style.textAlign = "center";
    icon.style.opacity = "0";
    icon.style.transform = "scale(0.6)";
    icon.style.transition = "opacity 0.3s ease, transform 0.3s ease";
    icon.title = "Open in new tab";
    icon.setAttribute("viewBox", "0 0 24 24");
    icon.style.outline = "5px solid #0000008a";
    icon.style.padding = "6px";
    icon.style.fill = "#fff";

    icon.innerHTML =
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M352 0c-12.9 0-24.6 7.8-29.6 19.8s-2.2 25.7 6.9 34.9L370.7 96 201.4 265.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L416 141.3l41.4 41.4c9.2 9.2 22.9 11.9 34.9 6.9s19.8-16.6 19.8-29.6V32c0-17.7-14.3-32-32-32H352zM80 32C35.8 32 0 67.8 0 112V432c0 44.2 35.8 80 80 80H400c44.2 0 80-35.8 80-80V320c0-17.7-14.3-32-32-32s-32 14.3-32 32V432c0 8.8-7.2 16-16 16H80c-8.8 0-16-7.2-16-16V112c0-8.8 7.2-16 16-16H192c17.7 0 32-14.3 32-32s-14.3-32-32-32H80z"/></svg>';

    iframe.parentNode.style.position = "relative";
    iframe.parentNode.appendChild(icon);

    icon.addEventListener("mouseover", () => {
      icon.style.opacity = "1";
      icon.style.transform = "scale(1)";
      setTimeout(() => {
        icon.style.opacity = "0";
        icon.style.transform = "scale(0.6)";
      }, 9000);
    });
    iframe.addEventListener("mouseover", () => {
      icon.style.opacity = "1";
      icon.style.transform = "scale(1)";
      setTimeout(() => {
        icon.style.opacity = "0";
        icon.style.transform = "scale(0.6)";
      }, 9000);
    });

    iframe.addEventListener("mouseout", () => {
      icon.style.opacity = "0";
      icon.style.transform = "scale(0.6)";
    });

    icon.addEventListener("click", () => {
      window.open(iframe.src + `?here=true`, "_blank");
    });

    iframe.setAttribute("data-overlay-added", "true");
  });
}
setInterval(addIframeOverlay, 1000);

/////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
function run(button, text = "") {
  const inputId = button.getAttribute("data-id");
  const input = document.getElementById(inputId);
  let given;
  if (text.length == 0) {
    if (inputId === "bida") {
      if (checkInputs()) {
        const today = new Date().toDateString();
        given = `title = ${title.value}, description of task = ${disc.value}, Category of task = ${Category.value}, deadline of task = ${Deadline.value} and -> today is ${today}`;
      } else {
        toast("d", "pleas fill all requared feilds");
      }
    } else {
      if (checkIn(input)) {
        given = input.value;
      } else {
        toast("w", "Please enter a text of at least 10 characters.");
      }
    }
  } else {
    if (checkIn(text)) {
      given = text;
    } else {
      toast("w", "Please enter a text of at least 10 characters.");
    }
  }
  const isValidInput =
    (inputId === "bida" && checkInputs()) ||
    input.value.replace(" ", "").length >= 10;

  if (isValidInput) {
    button.classList.add("run");
    fetch("/rephrase_text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        main: inputId,
        text: given,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        button.classList.remove("run");
        if (data.text.includes("Inappropriate language detected")) {
            toast("w", "Inappropriate language detected.");
        } else {
        if (inputId === "bida") {
          const { prices, remainingStr } = extractPrices(data.text);
          if (prices) {
            const paste = document.getElementById("paste");
            paste.style.display = "block";
            paste.setAttribute("data-arr", prices);
          } else {
            document.getElementById("paste").style.display = "none";
          }
          const re = remainingStr.replace("[", "").replace("]", "");
          document.getElementById("mtext").innerText = re;
          successModal.classList.remove("hidden");
          modalContent.classList.add("animate-scale");
        } else {
          toast("s", "Text rephreased successfully.");
          const re = data.text.replace("[", "").replace("]", "");
          input.value = re;
        }
      }})
      .catch((error) => {
        button.classList.remove("run");

        toast("d", "An Error occurred.");

        console.error("Error:", error);
      });
  }
}
function checkIn(input) {
  const emptyClass = "empty-field";
  let isEmpty = true;

  if (!(input.value.length >= 10)) {
    input.parentElement.classList.add(emptyClass);
    isEmpty = false;
  } else {
    input.parentElement.classList.remove(emptyClass);
  }

  return isEmpty;
}
function generateRandomString(length) {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
  let result = '';
  const charactersLength = characters.length;
  for (let i = 0; i < length; i++) {
      const randomIndex = Math.floor(Math.random() * charactersLength);
      result += characters.charAt(randomIndex);
  }
  return result;
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////


function showNotification(title, options) {
  if (!("Notification" in window)) {
      console.log("This browser does not support desktop notifications.");
      return;
  }
  
  const displayNotification = () => {
      const notification = new Notification(title, options);
      if (options.onClick) {
          notification.onclick = options.onClick;
      }
  };

  if (Notification.permission === "granted") {
      displayNotification();
  } else if (Notification.permission === "default") {
      Notification.requestPermission().then(permission => {
          if (permission === "granted") {
              displayNotification();
          }
      });
  } else {
      console.log("Notification permission denied.");
  }
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////

const ARRAY = [
  "Web Development",
  "Mobile App Development",
  "Software Development",
  "Game Development",
  "E-commerce Development",
  "Blockchain Development",
  "Artificial Intelligence",
  "Machine Learning",
  "Data Science",
  "Data Analysis",
  "Database Administration",
  "DevOps",
  "Cloud Computing",
  "Cybersecurity",
  "UI/UX Design",
  "Graphic Design",
  "Logo Design",
  "Illustration",
  "3D Modeling",
  "Animation",
  "Video Editing",
  "Motion Graphics",
  "Photography (Editing)",
  "Photo Editing",
  "Voice Over",
  "Music Production",
  "Sound Design",
  "Content Writing",
  "Copywriting",
  "Technical Writing",
  "Blog Writing",
  "Ghostwriting",
  "Translation",
  "Transcription",
  "Proofreading",
  "Editing",
  "Digital Marketing",
  "SEO",
  "Social Media Marketing",
  "Email Marketing",
  "Content Marketing",
  "Affiliate Marketing",
  "PPC Advertising",
  "Market Research",
  "Sales Strategy",
  "Business Development",
  "Lead Generation",
  "Customer Service",
  "Virtual Assistance",
  "Project Management",
  "Product Management",
  "Business Analysis",
  "Financial Analysis",
  "Accounting",
  "Bookkeeping",
  "Consulting",
  "Legal Services",
  "HR Services",
  "Recruitment",
  "Training and Development",
  "IT Support",
  "Technical Support",
  "Network Administration",
  "System Administration",
  "ERP/CRM Management",
  "Supply Chain Management",
  "Instructional Design",
  "Corporate Training",
  "E-learning Development",
  "Online Teaching",
  "Virtual Events",
  "Webinars",
  "Podcasting",
  "Blogging",
  "Vlogging",
  "Social Media Content",
  "Infographics",
  "Email Newsletters",
  "Chatbot Development",
  "Custom Software",
  "Plugin Development",
  "API Integration",
  "Custom Scripts",
  "Automation Services",
  "Data Entry",
  "Data Mining",
  "Data Cleansing",
  "Excel Services",
  "CRM Management",
  "Lead Management",
  "Cold Calling",
  "Telemarketing",
  "Customer Surveys",
  "User Testing",
  "Product Testing",
  "Market Analysis",
  "Competitor Analysis",
  "Industry Analysis",
  "Feasibility Studies",
  "Business Plans",
  "Pitch Decks",
  "Grant Writing",
  "Proposal Writing",
  "Resume Writing",
  "LinkedIn Profile Optimization",
  "Job Application Assistance",
  "Career Counseling",
  "Interview Coaching",
  "Mock Interviews",
  "Negotiation Coaching",
  "Public Speaking Coaching",
  "Voice Coaching",
  "Accent Reduction",
  "Language Instruction",
  "ESL Instruction",
  "Curriculum Development",
  "Educational Consultation",
  "Special Education Services",
  "Event Photography (Editing)",
  "Wedding Photography (Editing)",
  "Portrait Photography (Editing)",
  "Product Photography (Editing)",
  "Food Photography (Editing)",
  "Travel Photography (Editing)",
  "Real Estate Photography (Editing)",
  "Aerial Photography (Editing)",
  "Documentary Filmmaking (Editing)",
  "Corporate Videography (Editing)",
  "Event Videography (Editing)",
  "Promotional Videos (Editing)",
  "Explainer Videos",
  "Educational Videos",
  "YouTube Channel Management",
  "Podcast Editing",
  "Audio Editing",
  "Audiobook Production",
  "Jingle Creation",
  "Music Composition",
  "Sound Effects",
  "Voice Acting",
  "Narration",
  "Dubbing",
  "Subtitling",
  "Closed Captioning",
  "Live Interpretation",
  "Medical Transcription",
  "Legal Transcription",
  "Academic Transcription",
  "Market Research Analysis",
  "Survey Design",
  "Questionnaire Design",
  "Market Segmentation",
  "Brand Positioning",
  "Consumer Behavior Analysis",
  "Trend Analysis",
  "User Research",
  "Persona Development",
  "Wireframing",
  "Prototyping",
  "User Journey Mapping",
  "Accessibility Consulting",
  "Inclusive Design",
  "Design Thinking Workshops",
  "Agile Coaching",
  "Scrum Master Services",
  "Kanban Coaching",
  "Process Improvement",
  "Change Management",
  "Risk Management",
  "Quality Assurance",
  "Testing Services",
  "User Acceptance Testing",
  "Regression Testing",
  "Performance Testing",
  "Load Testing",
  "Security Testing",
  "Usability Testing",
  "Localization Testing",
  "Localization Services",
  "Cultural Consulting",
  "Global Marketing",
  "Patent Consulting",
  "Trademark Consulting",
  "Intellectual Property Consulting",
];
function OFC() {
  return ARRAY;
}
