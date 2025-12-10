"use client";
import { useState } from "react";
import { Menu, MenuItem, HoveredLink } from "@/components/ui/navbar-menu";
import { cn } from "@/lib/utils";

export default function Navbar({ className }: { className?: string }) {
  const [active, setActive] = useState<string | null>(null);

  return (
    <div
      className={cn(
        "fixed top-4 inset-x-0 max-w-xl mx-auto z-50",
        className,
        "backdrop-blur-md bg-black/30 border border-white/10",
        "rounded-xl shadow-lg"
      )}
    >
      <Menu setActive={setActive}>

        {/* ABOUT */}
        <MenuItem setActive={setActive} active={active} item="About">
          <div className="flex flex-col space-y-4 text-sm">
            <HoveredLink href="/about">
              <div className="flex items-center gap-2">
                <img src="/about.png" className="w-5 h-5" />
                <span>Who We Are</span>
              </div>
            </HoveredLink>

            <HoveredLink href="/team">
              <div className="flex items-center gap-2">
                <img src="/team.png" className="w-5 h-5" />
                <span>Team</span>
              </div>
            </HoveredLink>

            <HoveredLink href="/contact">
              <div className="flex items-center gap-2">
                <img src="/contact.png" className="w-5 h-5" />
                <span>Contact</span>
              </div>
            </HoveredLink>
          </div>
        </MenuItem>

        {/* LOGIN */}
        <MenuItem setActive={setActive} active={active} item="Login">
          <div className="flex flex-col space-y-4 text-sm">
            <HoveredLink href="/login/patient">
              <div className="flex items-center gap-2">
                <img src="/login.png" className="w-5 h-5" />
                <span>Patient Login</span>
              </div>
            </HoveredLink>

            <HoveredLink href="/login/doctor">
              <div className="flex items-center gap-2">
                <img src="/doctor.png" className="w-5 h-5" />
                <span>Doctor Login</span>
              </div>
            </HoveredLink>
          </div>
        </MenuItem>

        {/* REGISTER */}
        <MenuItem setActive={setActive} active={active} item="Register">
          <div className="flex flex-col space-y-4 text-sm">
            <HoveredLink href="/register/patient">
              <div className="flex items-center gap-2">
                <img src="/register.png" className="w-5 h-5" />
                <span>Patient Registration</span>
              </div>
            </HoveredLink>

            <HoveredLink href="/register/doctor">
              <div className="flex items-center gap-2">
                <img src="/doctor.png" className="w-5 h-5" />
                <span>Doctor Registration</span>
              </div>
            </HoveredLink>
          </div>
        </MenuItem>

      </Menu>
    </div>
  );
}
