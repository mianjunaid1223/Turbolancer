let chatPartner = null;
let selectedImage = null;
let replyToMessageId = null;
function scrollToBottom() {
    const messagesContainer = document.getElementById('messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

document.addEventListener('DOMContentLoaded', function () {
  const messages = document.getElementById('messages');
  const contextMenu = document.getElementById('contextMenu');
  const replyOption = document.getElementById('replyOption');
  const copyOption = document.getElementById('copyOption');
  const deleteOption = document.getElementById('deleteOption');
  let targetMessage = null;

  messages.addEventListener('contextmenu', function (e) {
    e.preventDefault();
    targetMessage = e.target.closest('.messP');
    if (targetMessage) {
      contextMenu.style.display = 'block';
      void contextMenu.offsetWidth;
      contextMenu.classList.add('show');

      const menuWidth = contextMenu.offsetWidth;
      const menuHeight = contextMenu.offsetHeight;
      const windowWidth = window.innerWidth;
      const windowHeight = window.innerHeight;

      let left = e.clientX;
      let top = e.clientY;

      if (left + menuWidth > windowWidth) {
        left = windowWidth - menuWidth - 10;
      }

      if (top + menuHeight > windowHeight) {
        top = windowHeight - menuHeight - 10;
      }

      left = Math.max(10, left);
      top = Math.max(10, top);

      contextMenu.style.left = `${left}px`;
      contextMenu.style.top = `${top}px`;

      deleteOption.style.display = (targetMessage.getAttribute('data-pop') === username) ? 'flex' : 'none';

      const isTextMessage = targetMessage.querySelector('.chat-bubble p') !== null && !targetMessage.querySelector('.chat-bubble.dell p');
      copyOption.style.display = isTextMessage ? 'flex' : 'none';
    }
  });

  document.addEventListener('click', function (e) {
    if (!contextMenu.contains(e.target)) {
      hideContextMenu();
    }
  });

  function hideContextMenu() {
    contextMenu.classList.remove('show');

    const transitionEndHandler = function () {
      contextMenu.style.display = 'none';
      contextMenu.removeEventListener('transitionend', transitionEndHandler);
    };

    contextMenu.addEventListener('transitionend', transitionEndHandler);
  }

  replyOption.addEventListener('click', function () {
    if (targetMessage) {
      reply(targetMessage);
      hideContextMenu();
    }
  });

  copyOption.addEventListener('click', function () {
    const textElement = targetMessage.querySelector('.chat-bubble p');
    if (textElement) {
      navigator.clipboard.writeText(textElement.innerText).then(() => {
        toast('s', 'Message copied to clipboard');
      }).catch(err => {
        toast('d', 'Failed to copy message');
      });
    }
    hideContextMenu();
  });

  deleteOption.addEventListener('click', function () {
    if (targetMessage) {
      hideContextMenu();

      modal('w', 'Are you sure you want to delete this message?', 'Yes, I\'m sure', 'dellit');
      document.querySelector('#dellit').addEventListener('click', function () {
        if (targetMessage.getAttribute('data-pop') === username) {
          const messageId = targetMessage.id;
          socket.emit('deleteMessage', { messageId, room, username });
        } else {
          toast('d', 'An error occurred');
        }
      });
    }
  });

  window.addEventListener('resize', function () {
    if (contextMenu.classList.contains('show')) {
      const menuRect = contextMenu.getBoundingClientRect();
      const windowWidth = window.innerWidth;
      const windowHeight = window.innerHeight;

      let left = parseInt(contextMenu.style.left);
      let top = parseInt(contextMenu.style.top);

      if (left + menuRect.width > windowWidth) {
        left = windowWidth - menuRect.width - 10;
      }
      if (top + menuRect.height > windowHeight) {
        top = windowHeight - menuRect.height - 10;
      }

      contextMenu.style.left = `${left}px`;
      contextMenu.style.top = `${top}px`;
    }
  });
});
const inputField = document.getElementById('message');

inputField.addEventListener('keypress', function (event) {
  if (event.keyCode === 13) {
    sendMessage();
  }
});


function joinRoom() {
  socket.emit('join', { username, room });
  resetChatHeader();
}

joinRoom();

window.addEventListener('beforeunload', () => {
  socket.disconnect();
});

socket.on('delDone', function (data) {
  const [message, usernameG, message_id] = data;
  ele = document.getElementById(message_id)
  if (ele) {
    ele.classList.add('deleted')
    ele.disabled = true
    ele.innerHTML = ''
    const alignmentClass = (usernameG === username) ? 'chat-end de' : 'chat-start de';

    ele.innerHTML = `<div class="chat ${alignmentClass}">
<div class="chat-bubble dell"><p>
${message}</p></div>
</div>`

  }
})
socket.on('status', function (data) {
  const messageContainer = document.getElementById('messages');

  if (data.id) {
    if (data.id !== username) {
      updateChatPartner(data, other = true);
    }
  }
});

function updateChatPartner(data, other = false) {
  chatPartner = data;

  const userImage = document.getElementById('Suser');
  const userHeader = document.getElementById('chat-header');
  const userStatus = document.getElementById('user-status');
  const messageContainer = document.getElementById('messages');

  if (other) {
    userImage.src = data.image;
    userHeader.innerText = data.name;
    const statusIndicator = document.createElement('span');
    statusIndicator.classList.add('status-indicator');
    statusIndicator.classList.toggle('status-online', data.online);
    statusIndicator.classList.toggle('status-offline', !data.online);
    userStatus.innerHTML = '';
    userStatus.appendChild(statusIndicator);
    userStatus.appendChild(document.createTextNode(`${data.online ? 'online (In chat)' : 'offline (Not in chat)'}`));
  }

  messageContainer.scrollTop = messageContainer.scrollHeight;
}

function resetChatHeader() {
  const userImage = document.getElementById('Suser');
  const userHeader = document.getElementById('chat-header');
  const userStatus = document.getElementById('user-status');

  userImage.src = '/static/avatar.svg';
  userHeader.innerText = 'Loading...';

  const statusIndicator = document.createElement('span');
  statusIndicator.classList.add('status-indicator', 'status-offline');
  userStatus.innerHTML = '';
  userStatus.appendChild(statusIndicator);
  userStatus.appendChild(document.createTextNode('offline (Not in chat)'));
}
// Send heartbeat every 30 seconds
setInterval(() => {
  socket.emit('heartbeat', { username: username, room: room });
}, 30000);

// Use Page Visibility API
document.addEventListener('visibilitychange', function() {
  if (document.hidden) {
    socket.emit('user_inactive', { username: username, room: room });
  } else {
    socket.emit('user_active', { username: username, room: room });
  }
});


socket.on('disconnect', function () {
  resetChatHeader();
  const userStatus = document.getElementById('user-status');
  const statusIndicator = document.createElement('span');
  statusIndicator.classList.add('status-indicator', 'status-offline');
  userStatus.innerHTML = '';
  userStatus.appendChild(statusIndicator);
  setTimeout(() => {
    socket.connect();
    // Re-join rooms and update status after reconnection
    socket.emit('Rejoin', { username: username, room: room });
  }, 5000);
  userStatus.appendChild(document.createTextNode('Reconnecting...'));
});
function remove(img){
img.onload= ()=>{
console.log('opened....')
}
}

function sendMessage() {
    sendbtn = document.getElementById('send-btn')
    sendbtn.classList.add('dis')
    const messageInput = document.getElementById('message');
    const message = messageInput.value.trim();
    if (message !== '' || selectedImage) {
      if (selectedImage) {
        const caption = message;
        socket.emit('message', { image: selectedImage, room, username, caption, replyTo: replyToMessageId });
        cancelImage();
      } else {
        socket.emit('message', { message, room, username, replyTo: replyToMessageId });
      }
      messageInput.value = '';
      cancelReply();
    }
  }
socket.on('response', function(data) {
    appendMessage(data)
    sendbtn = document.getElementById('send-btn')
    if (sendbtn){
        sendbtn.classList.remove('dis')

    }
  });
  function addeven(id){
    document.querySelector('#accept').onclick = () =>{handleOffer('accept', id)} 
    document.querySelector('#reject').onclick = () =>{handleOffer('reject', id)}
}

  function appendMessage(data) {
    const message = data.message;
    const sender = data.sender;
    const timestamp = data.timestamp;
    const type = data.type;
    const caption = data.caption || '';
    const replyTo = data.replyTo || null;
    const filename = data.filename || '';
   const isOwnMessage = sender === username;
    const messageContainer = document.getElementById('messages');
    
    const messageElement = document.createElement('div');
    messageElement.classList.add('messP');
    messageElement.addEventListener("dblclick", function () {
        reply(messageElement);
    });
  
    messageElement.id = timestamp;
    messageElement.setAttribute('data-pop', sender);
    messageElement.style.borderRadius = '10px';
    messageElement.style.padding = '10px';
  
    const alignmentClass = isOwnMessage ? 'chat-end' : 'chat-start';
  
    let messageContent = '';
    let localTime = convertToLocalTime(timestamp);
  
    switch (type) {
      case 'text':
        messageContent = `<div class="chat-bubble"><p>${message}</p></div>`;
        break;
      case 'image':
        messageContent = `
          <div class="chat-bubble">
            <img src="${message}" onload="document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight; remove(this)" onclick="openit(this)" alt="Image" class="max-w-xs h-auto rounded-lg">
            ${caption ? `<div class="text-sm mt-2"><p>${caption}</p></div>` : ''}
          </div>`;
        break;
      case 'offer':
        if (!isOwnMessage){
        showModal(message.split('[<>===pvsi{turbolancer}===<>]'),'Y3VzdG9taXplZA=='+btoa(sender) )
        addeven(timestamp)}
        messageContent = `
          <div class="chat-bubble bg-yellow-100 text-black dell">
            <p>Submitted an offer </p> 
          </div>`;
        break;
      case 'file':
        messageContent = `
          <div class="chat-bubble bg-blue-100 text-black" style="background:#DBEAFE;color:#000;">
           <a href="${message}" download="${filename}"> <span class="file"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M0 64C0 28.7 28.7 0 64 0H224V128c0 17.7 14.3 32 32 32H384V448c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V64zm384 64H256V0L384 128z"/></svg>
             File</span>
            <p>${filename}</p></a>
          </div>`;
        break;
      case 'deleted':
        localTime = ''
        messageElement.classList.add('deleted');
        messageElement.disabled = true;
        messageContent = `<div class="chat-bubble dell"><p>${message}</p></div>`;
        break;
      default:
        messageContent = `<div class="chat-bubble"><p>${message}</p></div>`;
    }
  
    const rptext = (() => {
      if (!replyTo) return '';
      const replyElement = document.getElementById(replyTo);
      if (!replyElement) return 'Deleted message';
  
      const textElement = replyElement.querySelector('.chat-bubble p');
      if (textElement) {
        const trimmedText = textElement.innerText.trim();
        return trimmedText.slice(0, 30) + (trimmedText.length > 30 ? '...' : '');
      }
  
      const imageElement = replyElement.querySelector('.chat-bubble img');
      return imageElement ? 'Image' : 'Deleted message';
    })();
  
    messageElement.innerHTML = `
      <div class="chat ${alignmentClass}">
        ${replyTo ? `<div onclick="scrollToMessage('${replyTo}')" class="chat-header replyto">Replying to <span class="font-semibold cursor-pointer">${rptext}</span></div>` : ''}
        ${messageContent}
        <div class="chat-footer opacity-50">${localTime}</div>
      </div>
    `;
  
    messageElement.style.marginTop = '13px';
    messageContainer.appendChild(messageElement);
    scrollToBottom();
  }
  

  
  function handleOffer(action, timestamp) {
    let message = action === 'accept' ? 'Offer has been accepted!' : ' Offer has been declined!';
    socket.emit('message', { room: room, message: message, username: username, replyTo: timestamp });
  }

function previewImage(input) {
  const file = input.files[0];
  var maxSize = 1 * 1024 * 1024;

  if (file && file.size <= maxSize) {
    const reader = new FileReader();
    reader.onload = function (e) {
      selectedImage = e.target.result;
      showImagePreview(selectedImage);
    };
    reader.readAsDataURL(file);
  }
  else{
    toast('d','File size cannot be larger then 1MB')
  }
}

function dropImage(event) {
    event.preventDefault();
    const files = event.dataTransfer.files;
    const maxSize = 1 * 1024 * 1024;
  
    if (files.length > 0 && files[0].size <= maxSize) {
      const reader = new FileReader();
      reader.onload = function (e) {
         selectedImage = e.target.result;
        const fileType = files[0].type.split('/')[1];
        const supportedTypes = ['png', 'jpg', 'jpeg'];
  
        if (supportedTypes.includes(fileType)) {
          showImagePreview(selectedImage);
        } else {
          toast('d', 'The provided image format is not supported.');
        }
      };
      reader.readAsDataURL(files[0]);
    } else {
      toast('d', 'File size cannot be larger than 1MB');
    }
  }

function showImagePreview(imageData) {
  document.querySelector('.reply').classList.add('mar');
  const preview = document.getElementById('imagePreview');
  preview.src = imageData;
  preview.style.display = 'block';
  document.getElementById('cancelImage').style.display = 'flex';
  document.getElementById('message').placeholder = "Add a caption... (optional)";
}

function cancelImage() {
  selectedImage = null;
  document.getElementById('imageInput').value = '';
  document.getElementById('imagePreview').style.display = 'none';
  document.querySelector('.reply').classList.remove('mar');
  document.getElementById('cancelImage').style.display = 'none';
  document.getElementById('message').placeholder = "Type your message or drop an image here...";
}

function convertToLocalTime(timestamp) {
    const date = new Date(timestamp);
    const options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true };
    return new Intl.DateTimeFormat(undefined, options).format(date);
  }
function reply(item) {
  cancelReply()
  const rp = document.querySelector('.reply');


  rp.querySelector('span').onclick = function () {
    scrollToMessage(item.id)
  }

  rp.classList.add('show');
  event.preventDefault();

  const messageText = item.querySelector('.chat-bubble p') ? item.querySelector('.chat-bubble p').innerText : 'IMAGE';
  rp.querySelector('span').querySelector('p').innerText = messageText;
  replyToMessageId = item.id;

}

function cancelReply() {
  const rp = document.querySelector('.reply');
  rp.classList.remove('show');
  replyToMessageId = null;

}


function scrollToMessage(messageId) {
  const targetMessage = document.getElementById(messageId);
  if (targetMessage) {
    targetMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    targetMessage.classList.add('bg-green-200');
    setTimeout(() => targetMessage.classList.remove('bg-green-200'), 2000);
  } else {
    toast('d', 'Original message not found');
  }
}



document.getElementById('imageInput').addEventListener('change', function () {
  previewImage(this);
});

document.body.addEventListener('dragover', function (event) {
  event.preventDefault();
  document.body.classList.add('imageover');
});

document.body.addEventListener('drop', function (event) {
  dropImage(event);
  document.body.classList.remove('imageover');
});

document.body.addEventListener('click', function () {
  document.body.classList.remove('imageover');
});




  function openFileInput() {
    document.getElementById('fileInput').click();
  }
  
  function sendFile(input) {
    const file = input.files[0];
    if (file.size > 1024 * 1024) { // 1MB
      alert("File size exceeds 1MB limit.");
      return;
    }
  
    const reader = new FileReader();
    reader.onload = function(e) {
      const fileData = e.target.result.split(',')[1];
      socket.emit('message', { room: room, file: fileData, filename: file.name, username: username });
    };
    reader.readAsDataURL(file);
  }

// Function to open the offer modal
function openOfferModal(x) {
  if(x){
details('/offer',true)


  }

}


function showModal(data,s) {
  const [title, price, description, revisions, delivery] = data
  const modal = document.getElementById('modal');
  const modalTitle = document.getElementById('modal-title');
  const modalPrice = document.getElementById('modal-price');
  const modalDescription = document.getElementById('modal-description');
  const modalRevisions = document.getElementById('modal-revisions');
  const modalDelivery = document.getElementById('modal-delivery');
  const acceptBtn = document.getElementById('accept');
  const declineBtn = document.getElementById('reject');

  modalTitle.textContent = title;
  modalPrice.textContent = `$${price}`;
  modalDescription.textContent = description;
  modalRevisions.textContent = revisions;
  modalDelivery.textContent = delivery;

  acceptBtn.addEventListener('click', () => {
      // Handle accept button click
      console.log('Offer accepted');
      modal.classList.remove('modal-open');
  });

  declineBtn.addEventListener('click', () => {
      // Handle decline button click
      console.log('Offer declined');
      modal.classList.remove('modal-open');
  });

  modal.classList.add('modal-open');
  
console.log(go(s))
  document.querySelector('#anchorM').href = go(s)
}