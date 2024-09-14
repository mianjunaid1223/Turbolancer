const navbar = document.getElementById("navbar");
const tabularParent = document.getElementById("tabular_parent");
const imgElement = document.getElementById("imga");
const body = document.body;

let currentGradient = 1;
let imageCount = 3;
const imageLinks = ["/static/3.png", "/static/1.png", "/static/2.png"];
let base64Array = [];


function scrollFunction() {
    const scrollTop = document.body.scrollTop > 2 || document.documentElement.scrollTop > 2
    console.log(scrollTop)
    if (scrollTop) {
        navbar.classList.add('scrolled')
        tabularParent.classList.add('open')
        tabularParent.style.right = "0%";
        tabularParent.style.width = "100%";
        tabularParent.style.borderRadius = "0%";
        tabularParent.style.top = '67px';
    } else {
        navbar.classList.remove('scrolled')
        tabularParent.classList.remove('open')

        tabularParent.style.right = "1%";
        tabularParent.style.width = "98%";
        tabularParent.style.top = '80%';
        tabularParent.style.borderRadius = "30px 30px 0 0";
    }
}
window.onscroll = function () {
    scrollFunction();
};

function loadImageAsBase64(url) {
    return fetch(url)
        .then(response => response.blob())
        .then(blob => new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result.split(",")[1]);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        }));
}

async function loadAllImages() {
    try {
        base64Array = await Promise.all(imageLinks.map(loadImageAsBase64));
        imgElement.src = `data:image/png;base64,${base64Array[0]}`;
    } catch (error) {
        console.error("Error loading images:", error);
    }
}

function changeGradient() {
    body.classList.remove(`gradient${currentGradient}`);
    currentGradient = (currentGradient % 3) + 1;
    body.classList.add(`gradient${currentGradient}`);

    imgElement.style.opacity = "0";
    setTimeout(() => {
        imgElement.src = `data:image/png;base64,${base64Array[imageCount - 1]}`;
        imgElement.style.opacity = "1";
        imageCount = imageCount === 1 ? 3 : imageCount - 1;
    }, 300);
}

loadAllImages();
setInterval(changeGradient, 8000);

// Add the select function for tab switching
window.select = function (element) {
    const tabs = document.querySelectorAll('.tab span');
    tabs.forEach(tab => tab.classList.remove('active'));
    const ems = document.querySelectorAll(`span[data="${element.getAttribute('data')}"]`);
    ems.forEach(item => {
        item.classList.add('active');
    });

    const iframes = document.querySelectorAll('#iframe');
    iframes.forEach(iframe => iframe.style.display = 'none');

    const data = element.getAttribute('data');
    if (data === 'projects') {
        document.querySelector('.proj').style.display = 'block';
    } else if (data === 'service') {
        document.querySelector('.getsearved').style.display = 'block';
    } else if (data === 'job') {
        document.querySelector('.upload_job_if').style.display = 'block';
    }
};
const anchor = document.querySelectorAll('#anchor');
anchor.forEach(element => {
element.href += `?referrer=${encodeURIComponent(btoa(window.location.href))}`;

});
function showIframe(element) {
  document.querySelector('.Mactive')?.classList.remove('Mactive');
  element.classList.add('Mactive');
  document.querySelector('.drawer').style.height = '100svh';
  const link = element.getAttribute('data-link');
  const iframe = document.querySelector('.iframe iframe');
  document.querySelector('.navbar').style.background = '#fff';
  document.querySelector('.navbar').style.borderBottom = '1px solid lightgray';
  document.querySelector('.navbar').querySelector('.btn').style.color = '#000';
  
  if ( !iframe?.src?.includes(link)) {
    iframe.src = link;
  }

  toggleElements('.page', 'block', '1');
  toggleElements('.full_page', 'none', '0');

  const iframeContainer = document.querySelector('.iframe');
  iframeContainer.style.display = 'block';
  setTimeout(() => {
    iframeContainer.style.opacity = '1';
  }, 10);
  document.querySelector('.drawer-overlay').click()
}

function hideIframe(element) {
  document.querySelector('.navbar').style.borderBottom = '';

  document.querySelector('.navbar').querySelector('.btn').style.color = '#fff';
  document.querySelector('.navbar').style.background = '';
  document.querySelector('.drawer').style.height = '101svh';

  document.querySelector('.Mactive')?.classList.remove('Mactive');
  element.classList.add('Mactive');

  toggleElements('.page', 'none', '0');
  toggleElements('.full_page', 'block', '1');
  document.querySelector('.drawer-overlay').click()

}

function toggleElements(selector, displayValue, opacityValue) {
  document.querySelectorAll(selector).forEach(item => {
    item.style.opacity = opacityValue === '1' ? '0' : '1';
    setTimeout(() => {
      item.style.display = displayValue;
      item.style.opacity = opacityValue;
    }, 10);
  });
}