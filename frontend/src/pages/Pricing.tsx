import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Check, X } from "lucide-react";

const PRICING_TIERS = [
    {
        name: "Initiate",
        price: "Free",
        period: "Forever",
        description: "Perfect for individual creators exploring the temple",
        features: [
            { name: "10 downloads per day", included: true },
            { name: "5 conversions per day", included: true },
            { name: "30 minutes transcription/month", included: true },
            { name: "2GB cloud storage", included: true },
            { name: "Standard processing speed", included: true },
            { name: "Community support", included: true },
            { name: "API access", included: false },
            { name: "Priority processing", included: false },
            { name: "Team collaboration", included: false },
            { name: "Custom branding", included: false }
        ],
        cta: "Start Free",
        ctaLink: "/register",
        popular: false
    },
    {
        name: "Priest",
        price: "$19",
        period: "per month",
        description: "For professionals who need unlimited power",
        features: [
            { name: "Unlimited downloads", included: true },
            { name: "Unlimited conversions", included: true },
            { name: "500 minutes transcription/month", included: true },
            { name: "50GB cloud storage", included: true },
            { name: "Priority processing speed", included: true },
            { name: "Priority email support", included: true },
            { name: "Full API access", included: true },
            { name: "Batch processing", included: true },
            { name: "Advanced analytics", included: true },
            { name: "Custom branding", included: false }
        ],
        cta: "Start 14-Day Trial",
        ctaLink: "/register?plan=priest",
        popular: true
    },
    {
        name: "Pharaoh",
        price: "$99",
        period: "per month",
        description: "For teams and enterprises ruling their domain",
        features: [
            { name: "Everything in Priest, plus:", included: true },
            { name: "Unlimited transcription", included: true },
            { name: "100GB cloud storage", included: true },
            { name: "Team collaboration (up to 10 users)", included: true },
            { name: "Custom branding", included: true },
            { name: "Dedicated account manager", included: true },
            { name: "SLA guarantee (99.9%)", included: true },
            { name: "Advanced security features", included: true },
            { name: "Custom integrations", included: true },
            { name: "White-label API", included: true }
        ],
        cta: "Contact Sales",
        ctaLink: "/contact",
        popular: false
    }
];

export const Pricing = () => {
    return (
        <div className="relative min-h-screen flex flex-col pb-24">
            {/* Hero Section */}
            <section className="container mx-auto px-4 pt-20 pb-16 text-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="space-y-6"
                >
                    <h1 className="text-5xl md:text-6xl font-heading font-bold text-transparent bg-clip-text bg-gradient-to-r from-papyrus via-gold to-papyrus">
                        Choose Your Path
                    </h1>
                    <p className="text-xl text-sand max-w-3xl mx-auto">
                        Select the perfect plan for your journey. All plans include our core features with a 14-day money-back guarantee.
                    </p>
                </motion.div>
            </section>

            {/* Pricing Cards */}
            <section className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-7xl mx-auto">
                    {PRICING_TIERS.map((tier, index) => (
                        <motion.div
                            key={tier.name}
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className={tier.popular ? "md:-mt-8" : ""}
                        >
                            <PricingCard {...tier} />
                        </motion.div>
                    ))}
                </div>
            </section>

            {/* FAQ Section */}
            <section className="container mx-auto px-4 mt-24">
                <div className="text-center mb-12">
                    <h2 className="text-3xl md:text-4xl font-heading font-bold text-gold mb-4">
                        Frequently Asked Questions
                    </h2>
                </div>

                <div className="max-w-3xl mx-auto space-y-4">
                    <FAQItem
                        question="Can I change my plan at any time?"
                        answer="Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately, and we'll prorate any payments."
                    />
                    <FAQItem
                        question="What payment methods do you accept?"
                        answer="We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and bank transfers for enterprise plans."
                    />
                    <FAQItem
                        question="Is there a free trial?"
                        answer="Yes! All paid plans come with a 14-day free trial. No credit card required to start the Initiate plan."
                    />
                    <FAQItem
                        question="What happens to my files if I cancel?"
                        answer="You'll have 30 days to download your files from cloud storage before they're permanently deleted."
                    />
                    <FAQItem
                        question="Do you offer refunds?"
                        answer="Yes, we offer a 14-day money-back guarantee on all paid plans, no questions asked."
                    />
                </div>
            </section>

            {/* CTA Section */}
            <section className="container mx-auto px-4 mt-24">
                <div className="bg-gradient-to-r from-temple to-obsidian border border-gold/20 rounded-3xl p-12 text-center">
                    <h2 className="text-4xl font-heading font-bold text-papyrus mb-4">
                        Still Have Questions?
                    </h2>
                    <p className="text-xl text-sand mb-8 max-w-2xl mx-auto">
                        Our team is here to help you find the perfect plan for your needs.
                    </p>
                    <Link to="/contact">
                        <Button size="lg" className="text-lg px-12">
                            Contact Sales
                        </Button>
                    </Link>
                </div>
            </section>
        </div>
    );
};

import { ScepterButton } from "../components/pharaonic/ScepterButton";

const PricingCard = ({ name, price, period, description, features, cta, ctaLink, popular }: typeof PRICING_TIERS[0]) => (
    <Card className={`h-full flex flex-col relative overflow-hidden bg-papyrus-texture border border-obsidian/10 ${popular
        ? "scale-105 shadow-[0_0_50px_rgba(209,174,118,0.4)] z-10 brightness-110 sepia-0"
        : "shadow-2xl brightness-110 sepia-0"
        }`}>
        {popular && (
            <div className="absolute top-0 right-0 bg-gold text-obsidian px-6 py-2 rounded-bl-xl text-sm font-bold font-heading z-20 shadow-md">
                Chosen by the Gods
            </div>
        )}

        <CardHeader className="text-center pb-8 pt-8 relative z-10">
            {/* Hieroglyphic decoration at top - using brand colors */}
            <div className="w-16 h-1 bg-obsidian/20 mx-auto mb-6" />

            <CardTitle className="text-3xl font-heading text-obsidian mb-2 drop-shadow-sm tracking-wide">{name}</CardTitle>
            <div className="mb-4">
                <span className="text-5xl font-heading font-bold text-obsidian drop-shadow-sm">{price}</span>
                {period !== "Forever" && <span className="text-obsidian/80 font-heading ml-1 text-lg">/{period}</span>}
                {period === "Forever" && <span className="text-obsidian/80 font-heading ml-1 block text-sm mt-1 uppercase tracking-widest">{period}</span>}
            </div>
            <CardDescription className="text-base text-obsidian/70 italic font-medium">{description}</CardDescription>
        </CardHeader>

        <CardContent className="flex-1 flex flex-col relative z-10">
            <div className="w-full h-px bg-obsidian/10 mb-6" />
            <ul className="space-y-4 mb-8 flex-1">
                {features.map((feature, i) => (
                    <li key={i} className="flex items-start gap-3">
                        {feature.included ? (
                            <Check className="w-5 h-5 text-obsidian flex-shrink-0 mt-0.5 stroke-[3]" />
                        ) : (
                            <X className="w-5 h-5 text-obsidian/20 flex-shrink-0 mt-0.5" />
                        )}
                        <span className={feature.included ? "text-obsidian font-medium" : "text-obsidian/40 line-through decoration-obsidian/20"}>
                            {feature.name}
                        </span>
                    </li>
                ))}
            </ul>

            <Link to={ctaLink} className="block mt-auto">
                <ScepterButton
                    variant={popular ? "primary" : "secondary"}
                    className={`w-full text-lg h-14 ${!popular && "border-obsidian text-obsidian hover:bg-obsidian hover:text-gold"}`}
                >
                    {cta}
                </ScepterButton>
            </Link>
        </CardContent>
    </Card>
);

const FAQItem = ({ question, answer }: { question: string; answer: string }) => (
    <Card className="bg-temple/50 backdrop-blur-sm border-gold/10">
        <CardHeader>
            <CardTitle className="text-lg">{question}</CardTitle>
        </CardHeader>
        <CardContent>
            <p className="text-sand">{answer}</p>
        </CardContent>
    </Card>
);
