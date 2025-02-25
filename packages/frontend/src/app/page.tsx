import Chat from "@/pages/Chat";
import { Toaster } from "react-hot-toast";
export default async function Home() {
  // const data = await fetch(`http://backend:8000/api/load`, { method: 'GET' });
  // const json = await data.json();
  // console.log(json);

  return (
    <>
      <Chat />
      <Toaster />
    </>
  );
}
