import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { MapPin, Mail, Phone, Send } from "lucide-react";

export const Contact = () => {
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
                        Reach the Oracle
                    </h1>
                    <p className="text-xl text-sand max-w-3xl mx-auto">
                        Have questions or need assistance? Our team of scribes is ready to help you on your journey.
                    </p>
                </motion.div>
            </section>

            <div className="container mx-auto px-4">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Contact Form */}
                    <Card className="lg:col-span-2 bg-temple/50 backdrop-blur-sm border-gold/10">
                        <CardHeader>
                            <CardTitle>Send Us a Message</CardTitle>
                            <CardDescription>Fill out the form below and we'll get back to you within 24 hours</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form className="space-y-6">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <Input placeholder="First Name" />
                                    <Input placeholder="Last Name" />
                                </div>

                                <Input type="email" placeholder="Email Address" />

                                <Input placeholder="Subject" />

                                <div>
                                    <textarea
                                        placeholder="Your Message"
                                        rows={6}
                                        className="w-full px-4 py-3 bg-obsidian border border-gold/20 rounded-lg text-papyrus placeholder:text-sand/50 focus:border-gold focus:outline-none resize-none"
                                    />
                                </div>

                                <Button type="submit" className="w-full text-lg h-12">
                                    <Send className="w-5 h-5 mr-2" />
                                    Send Message
                                </Button>
                            </form>
                        </CardContent>
                    </Card>

                    {/* Contact Info */}
                    <div className="space-y-6">
                        {/* Office Location */}
                        <Card className="bg-temple/50 backdrop-blur-sm border-gold/10">
                            <CardHeader>
                                <div className="flex items-center gap-3 mb-2">
                                    <div className="p-2 bg-obsidian rounded-lg">
                                        <MapPin className="w-5 h-5 text-gold" />
                                    </div>
                                    <CardTitle className="text-lg">Temple Location</CardTitle>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sand">
                                    Valley of the Kings<br />
                                    Luxor, Egypt<br />
                                    Ancient Realm
                                </p>
                            </CardContent>
                        </Card>

                        {/* Email */}
                        <Card className="bg-temple/50 backdrop-blur-sm border-gold/10">
                            <CardHeader>
                                <div className="flex items-center gap-3 mb-2">
                                    <div className="p-2 bg-obsidian rounded-lg">
                                        <Mail className="w-5 h-5 text-gold" />
                                    </div>
                                    <CardTitle className="text-lg">Email</CardTitle>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <a href="mailto:contact@voith.temple" className="text-gold hover:underline">
                                    contact@voith.temple
                                </a>
                                <p className="text-sand text-sm mt-2">
                                    We'll respond within 24 hours
                                </p>
                            </CardContent>
                        </Card>

                        {/* Phone */}
                        <Card className="bg-temple/50 backdrop-blur-sm border-gold/10">
                            <CardHeader>
                                <div className="flex items-center gap-3 mb-2">
                                    <div className="p-2 bg-obsidian rounded-lg">
                                        <Phone className="w-5 h-5 text-gold" />
                                    </div>
                                    <CardTitle className="text-lg">Phone</CardTitle>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <a href="tel:+20123456789" className="text-gold hover:underline">
                                    +20 123 456 789
                                </a>
                                <p className="text-sand text-sm mt-2">
                                    Mon-Fri: 9am - 6pm (GMT+2)
                                </p>
                            </CardContent>
                        </Card>

                        {/* Business Hours */}
                        <Card className="bg-temple/50 backdrop-blur-sm border-gold/10">
                            <CardHeader>
                                <CardTitle className="text-lg">Business Hours</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-2 text-sm">
                                    <div className="flex justify-between">
                                        <span className="text-sand">Monday - Friday</span>
                                        <span className="text-papyrus">9:00 - 18:00</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-sand">Saturday</span>
                                        <span className="text-papyrus">10:00 - 14:00</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-sand">Sunday</span>
                                        <span className="text-papyrus">Closed</span>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </div>

            {/* Support Section */}
            <section className="container mx-auto px-4 mt-16">
                <Card className="bg-gradient-to-r from-temple to-obsidian border-gold/20">
                    <CardContent className="p-12 text-center">
                        <h2 className="text-3xl font-heading font-bold text-papyrus mb-4">
                            Need Immediate Help?
                        </h2>
                        <p className="text-sand mb-8 max-w-2xl mx-auto">
                            Check out our comprehensive documentation and FAQ section for instant answers to common questions.
                        </p>
                        <div className="flex gap-4 justify-center flex-wrap">
                            <Button variant="secondary" size="lg">
                                View Documentation
                            </Button>
                            <Button variant="secondary" size="lg">
                                Visit Help Center
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </section>
        </div>
    );
};
