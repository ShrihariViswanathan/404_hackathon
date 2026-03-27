import {
  SignedIn,
  SignedOut,
  SignInButton,
  useClerk,
} from "@clerk/clerk-react";import { motion } from 'framer-motion'

import React from 'react'

const Header = () => {
  return (
    <>
    <div className="w-full px-8 py-4 flex items-center justify-between 
                   bg-gradient-to-r from-[#0f2a4a] to-[#020817] border-b ">

      {/* Logo */}
      <motion.h1
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-2xl font-bold tracking-wide bg-gradient-to-r 
                   from-blue-400 to-purple-500 bg-clip-text text-transparent"
      >
        TradeCraft
      </motion.h1>

      

   <div>
      {/* If user NOT logged in */}
      <SignedOut>
        <SignInButton mode="modal">
          <button className="rounded-lg fill-blue-950" style={{ padding: "8px 16px" }}>
            Login
          </button>
        </SignInButton>
      </SignedOut>

      {/* If user logged in */}
      <SignedIn>
        <button
          onClick={() => signOut()}
          style={{ padding: "8px 16px" }}
        >
          Logout
        </button>
      </SignedIn>
    </div>
    </div>
    </>
  )
}

export default Header
