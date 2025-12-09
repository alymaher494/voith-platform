import * as React from "react";
import { cn } from "../../lib/utils";

export interface InputProps
    extends React.InputHTMLAttributes<HTMLInputElement> { }

const Input = React.forwardRef<HTMLInputElement, InputProps>(
    ({ className, type, ...props }, ref) => {
        return (
            <div className="relative group">
                <input
                    type={type}
                    className={cn(
                        "flex h-12 w-full border-b border-gold/30 bg-transparent px-3 py-2 text-sm ring-offset-obsidian file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-transparent focus-visible:outline-none focus-visible:border-gold focus-visible:ring-0 disabled:cursor-not-allowed disabled:opacity-50 peer transition-all text-papyrus",
                        className
                    )}
                    ref={ref}
                    placeholder={props.placeholder || "Input"}
                    {...props}
                />
                <label className="absolute left-3 -top-3.5 text-xs text-gold transition-all peer-placeholder-shown:text-base peer-placeholder-shown:text-sand peer-placeholder-shown:top-3 peer-focus:-top-3.5 peer-focus:text-xs peer-focus:text-gold pointer-events-none">
                    {props.placeholder}
                </label>
                <div className="absolute bottom-0 left-0 w-0 h-[2px] bg-gold transition-all duration-300 peer-focus:w-full" />
            </div>
        );
    }
);
Input.displayName = "Input";

export { Input };
