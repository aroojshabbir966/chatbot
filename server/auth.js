const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const nodemailer = require('nodemailer');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Nodemailer setup (replace with your email configuration)
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'your-email@gmail.com',
    pass: 'your-email-password',
  },
});

// Handling socket connections
io.on('connection', (socket) => {
  console.log('A user connected');

  // Listen for chat messages
  socket.on('chat message', (msg) => {
    // Check if the message contains a special command
    if (msg.startsWith('/sendEmail')) {
      sendEmailNotification(msg);
    }

    // Broadcast the message to all connected clients
    io.emit('chat message', msg);
  });

  // Listen for disconnections
  socket.on('disconnect', () => {
    console.log('User disconnected');
  });
});

// Function to send email notification
function sendEmailNotification(message) {
  const mailOptions = {
    from: 'your-email@gmail.com',
    to: 'recipient-email@example.com',
    subject: 'Chatbot Notification',
    text: `A user sent a special command: ${message}`,
  };

  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.error('Error sending email:', error);
    } else {
      console.log('Email sent:', info.response);
    }
  });
}

const port = process.env.PORT || 3000;

server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
