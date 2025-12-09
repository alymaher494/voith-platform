import { useRef, useEffect } from "react";
import { Button, ButtonProps } from "./Button";
import { gsap } from "../../lib/gsap";

interface MagneticButtonProps extends ButtonProps {
    strength?: number; // How strong the magnetic pull is (default: 0.5)
}

export const MagneticButton = ({ strength = 0.5, children, className, ...props }: MagneticButtonProps) => {
    const buttonRef = useRef<HTMLButtonElement>(null);

    useEffect(() => {
        const button = buttonRef.current;
        if (!button) return;

        const ctx = gsap.context(() => {
            // Magnetic effect
            const handleMouseMove = (e: MouseEvent) => {
                const rect = button.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;

                gsap.to(button, {
                    x: x * strength,
                    y: y * strength,
                    duration: 0.3,
                    ease: "power2.out"
                });
            };

            const handleMouseLeave = () => {
                gsap.to(button, {
                    x: 0,
                    y: 0,
                    duration: 0.5,
                    ease: "elastic.out(1, 0.3)"
                });
            };

            button.addEventListener("mousemove", handleMouseMove);
            button.addEventListener("mouseleave", handleMouseLeave);

            // Cleanup
            return () => {
                button.removeEventListener("mousemove", handleMouseMove);
                button.removeEventListener("mouseleave", handleMouseLeave);
            };
        }, buttonRef);

        return () => ctx.revert();
    }, [strength]);

    return (
        <Button ref={buttonRef} className={className} {...props}>
            {children}
        </Button>
    );
};
