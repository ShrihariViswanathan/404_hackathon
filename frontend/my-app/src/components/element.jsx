
import { Outlet } from "react-router-dom";
import Header from "./header";

export default function Layout() {
  return (
    <div className="bg-black min-h-screen font-sans text-white">
      <Header />
      <Outlet />
    </div>
  );
}