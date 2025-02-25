"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";

const API_URL = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL;

export default function Home() {
  const [message, setMessage] = useState("");

  const handleSendMessage = async () => {
    const response = await fetch(`${API_URL}/api/test`, {
      method: 'GET',
      headers: {
        'Accept': 'text/event-stream'
      }
    });

    const reader = response.body?.getReader();
    if (!reader) return;

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        console.log('Done');
        break;
      }
      
      // Convert the chunk to text and append to message
      const chunk = new TextDecoder().decode(value);
      setMessage((prev: string) => prev + chunk);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold">Hello World</h1>

      <Button onClick={handleSendMessage}>
        Send Message
      </Button>

      <p>
        {message}
      </p>
    </div>
  );
}
