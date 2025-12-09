import { motion } from "framer-motion";
import { useEffect, useState } from "react";

const HIEROGLYPHS = [
    "𓃥", "𓃠", "𓃰", "𓃱", "𓃯", "𓃭", "𓃸", "𓃵", "𓃗", "𓃘", "𓃙", "𓃟", "𓄀", "𓄁", "𓄂", "𓄃", "𓃚", "𓃛", "𓃜", "𓃝", "𓃞",
    "𓃒", "𓃓", "𓃔", "𓃕", "𓃖", "𓃡", "𓃢", "𓃦", "𓃩", "𓃫", "𓃬", "𓃮", "𓃲", "𓃴", "𓃶", "𓃷", "𓃹", "𓃻", "𓃽", "𓃾", "𓃿",
    "𓄄", "𓄅", "𓄆", "𓄇", "𓆇", "𓆈", "𓆉", "𓆌", "𓆏", "𓆗", "𓆘", "𓆙", "𓆚", "𓆐", "𓆑", "𓆒", "𓆓", "𓆔", "𓆕", "𓆖",
    "𓆊", "𓆍", "𓆣", "𓆤", "𓆥", "𓆦", "𓆧", "𓆨", "𓆛", "𓆜", "𓆝", "𓆞", "𓆟", "𓆠", "𓆡", "𓆢", "𓄿", "𓅀", "𓅁", "𓅂",
    "𓅃", "𓅄", "𓅅", "𓅆", "𓅇", "𓅈", "𓅉", "𓅋", "𓅌", "𓅍", "𓅎", "𓅏", "𓅐", "𓅑", "𓅒", "𓅓", "𓅔", "𓅕", "𓅖",
    "𓅗", "𓅘", "𓅙", "𓅚", "𓅛", "𓅜", "𓅝", "𓅞", "𓅟", "𓅠", "𓅢", "𓅣", "𓅤", "𓅥", "𓅦", "𓅧", "𓅨", "𓅩", "𓅪", "𓅫",
    "𓅬", "𓅭", "𓅮", "𓅯", "𓅰", "𓅱", "𓅲", "𓅳", "𓅴", "𓅵", "𓅷", "𓅶", "𓅸", "𓅹", "𓅺", "𓅻", "𓅼", "𓅽", "𓅾", "𓅿",
    "𓆀", "𓆁", "𓆂", "𓆃", "𓆆"
];
export const LivingBackground = () => {
    const [columns, setColumns] = useState<string[][]>([]);

    useEffect(() => {
        // Create 12 columns
        const newColumns = Array.from({ length: 12 }).map(() =>
            // Fill each column with 20 random glyphs
            Array.from({ length: 20 }).map(() =>
                HIEROGLYPHS[Math.floor(Math.random() * HIEROGLYPHS.length)]
            )
        );
        setColumns(newColumns);
    }, []);

    return (
        <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none select-none bg-obsidian flex justify-between px-4 opacity-60">
            {columns.map((col, i) => (
                <motion.div
                    key={i}
                    className="flex flex-col items-center gap-8 text-gold/30"
                    initial={{ y: i % 2 === 0 ? -100 : 0 }}
                    animate={{
                        y: i % 2 === 0 ? [0, -50, 0] : [-50, 0, -50]
                    }}
                    transition={{
                        duration: 20 + Math.random() * 10,
                        repeat: Infinity,
                        ease: "easeInOut"
                    }}
                >
                    {/* Vertical Line Separator (Optional, subtle) */}
                    <div className="absolute h-full w-[1px] bg-gold/5 -left-4" />

                    {col.map((char, j) => (
                        <div
                            key={j}
                            className="text-4xl font-serif transform transition-all duration-1000"
                            style={{
                                textShadow: "0 0 10px rgba(209, 174, 118, 0.1)"
                            }}
                        >
                            {char}
                        </div>
                    ))}
                </motion.div>
            ))}

            {/* Gradient Overlay for depth */}
            <div className="absolute inset-0 bg-gradient-to-b from-obsidian via-transparent to-obsidian" />
            <div className="absolute inset-0 bg-gradient-to-r from-obsidian/50 via-transparent to-obsidian/50" />
        </div>
    );
};
