# Taskie Chatbot Integration

## Overview
The Taskie chatbot has been integrated into the TaskBox dashboard as a floating chat widget. This allows users to interact with the AI assistant without leaving the main dashboard page.

## Features
- Floating chat icon positioned at the bottom-right corner of the screen
- Smooth open/close animations for the chat panel
- Responsive design that works on both desktop and mobile devices
- Seamless integration with existing dashboard functionality
- Consistent styling that matches the TaskBox theme

## Implementation Details
- The chat widget is implemented in `src/pages/dashboard.tsx`
- Uses the existing `ChatInterface` component from `src/components/ChatInterface.tsx`
- Communicates with the backend via the existing `/chat` endpoint
- Maintains all existing dashboard functionality while adding the chat feature

## How It Works
1. A floating chat icon is displayed at the bottom-right of the dashboard
2. Clicking the icon opens a chat panel with the Taskie assistant
3. Users can interact with the chatbot to manage their tasks
4. The chat panel can be closed without affecting the dashboard content
5. The chat functionality uses the existing backend API at `/chat`

## Styling
- The chat widget uses the same gradient colors as the rest of the application (blue to purple)
- Responsive design ensures proper display on all screen sizes
- Smooth transitions for opening and closing the chat panel
- Consistent with the overall TaskBox UI/UX design