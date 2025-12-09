import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Calendar, User, ArrowRight, Tag } from "lucide-react";

const BLOG_POSTS = [
    {
        id: 1,
        title: "Introducing VOITH: The Future of Media Processing",
        excerpt: "We're excited to announce the launch of VOITH, a revolutionary platform that combines ancient wisdom with modern AI to transform how you work with media.",
        author: "The VOITH Team",
        date: "November 15, 2025",
        category: "Announcements",
        image: "/src/assets/hero-thoth.png",
        slug: "introducing-voith"
    },
    {
        id: 2,
        title: "How AI Transcription is Changing Content Creation",
        excerpt: "Discover how OpenAI's Whisper model is revolutionizing speech-to-text conversion and why accuracy matters more than ever.",
        author: "Sarah Chen",
        date: "November 10, 2025",
        category: "AI & Technology",
        image: "/src/assets/logo-icon.png",
        slug: "ai-transcription-guide"
    },
    {
        id: 3,
        title: "5 Tips for Faster Video Downloads",
        excerpt: "Learn how to maximize your download speeds and get the highest quality content from any platform.",
        author: "Michael Torres",
        date: "November 5, 2025",
        category: "Tutorials",
        image: "/src/assets/logo-icon.png",
        slug: "faster-video-downloads"
    },
    {
        id: 4,
        title: "Understanding Video Codecs: H.264 vs H.265 vs AV1",
        excerpt: "A comprehensive guide to modern video codecs and which one you should use for your projects.",
        author: "Alex Kumar",
        date: "October 28, 2025",
        category: "Education",
        image: "/src/assets/logo-icon.png",
        slug: "video-codecs-explained"
    },
    {
        id: 5,
        title: "Building a SaaS Platform: Lessons from VOITH",
        excerpt: "Behind the scenes look at how we built VOITH and the technical decisions that shaped our platform.",
        author: "The VOITH Team",
        date: "October 20, 2025",
        category: "Engineering",
        image: "/src/assets/logo-icon.png",
        slug: "building-voith"
    },
    {
        id: 6,
        title: "The Ancient Egyptian Influence in Our Design",
        excerpt: "Exploring how we incorporated pharaonic aesthetics into a modern web application.",
        author: "Design Team",
        date: "October 15, 2025",
        category: "Design",
        image: "/src/assets/logo-full.png",
        slug: "pharaonic-design"
    }
];

const CATEGORIES = ["All", "Announcements", "AI & Technology", "Tutorials", "Education", "Engineering", "Design"];

export const Blog = () => {
    return (
        <div className="relative min-h-screen flex flex-col pb-24">
            {/* Hero Section */}
            <section className="container mx-auto px-4 pt-20 pb-16">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="text-center space-y-6"
                >
                    <h1 className="text-5xl md:text-6xl font-heading font-bold text-transparent bg-clip-text bg-gradient-to-r from-papyrus via-gold to-papyrus">
                        The Scroll of Knowledge
                    </h1>
                    <p className="text-xl text-sand max-w-3xl mx-auto">
                        Insights, tutorials, and stories from the VOITH temple. Learn how to master media processing and stay updated on the latest features.
                    </p>
                </motion.div>
            </section>

            {/* Categories */}
            <section className="container mx-auto px-4 mb-12">
                <div className="flex gap-3 flex-wrap justify-center">
                    {CATEGORIES.map((category) => (
                        <button
                            key={category}
                            className={`px-4 py-2 rounded-lg border-2 transition-all ${category === "All"
                                    ? "border-gold bg-gold/10 text-gold"
                                    : "border-gold/20 text-sand hover:border-gold/40"
                                }`}
                        >
                            {category}
                        </button>
                    ))}
                </div>
            </section>

            {/* Featured Post */}
            <section className="container mx-auto px-4 mb-16">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <Card className="bg-temple/50 backdrop-blur-sm border-gold/10 hover:border-gold/40 transition-all overflow-hidden">
                        <div className="grid md:grid-cols-2 gap-8">
                            <div className="h-64 md:h-auto bg-gradient-to-br from-gold/20 to-temple flex items-center justify-center">
                                <div className="text-6xl">𓁹</div>
                            </div>
                            <div className="p-8 flex flex-col justify-center">
                                <div className="flex items-center gap-4 mb-4">
                                    <span className="px-3 py-1 bg-gold/10 border border-gold/20 rounded-full text-xs text-gold">
                                        Featured
                                    </span>
                                    <span className="text-sm text-sand">{BLOG_POSTS[0].category}</span>
                                </div>
                                <h2 className="text-3xl font-heading font-bold text-papyrus mb-4">
                                    {BLOG_POSTS[0].title}
                                </h2>
                                <p className="text-sand mb-6">
                                    {BLOG_POSTS[0].excerpt}
                                </p>
                                <div className="flex items-center gap-4 text-sm text-sand mb-6">
                                    <div className="flex items-center gap-2">
                                        <User className="w-4 h-4" />
                                        {BLOG_POSTS[0].author}
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <Calendar className="w-4 h-4" />
                                        {BLOG_POSTS[0].date}
                                    </div>
                                </div>
                                <Link to={`/blog/${BLOG_POSTS[0].slug}`}>
                                    <Button>
                                        Read More <ArrowRight className="ml-2 w-4 h-4" />
                                    </Button>
                                </Link>
                            </div>
                        </div>
                    </Card>
                </motion.div>
            </section>

            {/* Blog Grid */}
            <section className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {BLOG_POSTS.slice(1).map((post, index) => (
                        <motion.div
                            key={post.id}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                        >
                            <BlogCard {...post} />
                        </motion.div>
                    ))}
                </div>
            </section>

            {/* Newsletter CTA */}
            <section className="container mx-auto px-4 mt-24">
                <Card className="bg-gradient-to-r from-temple to-obsidian border-gold/20">
                    <CardContent className="p-12 text-center">
                        <h2 className="text-3xl font-heading font-bold text-papyrus mb-4">
                            Subscribe to Our Scrolls
                        </h2>
                        <p className="text-sand mb-8 max-w-2xl mx-auto">
                            Get the latest insights and updates delivered to your inbox every week.
                        </p>
                        <div className="flex gap-4 max-w-md mx-auto">
                            <input
                                type="email"
                                placeholder="Enter your email"
                                className="flex-1 h-12 px-4 bg-obsidian border border-gold/20 rounded-lg text-papyrus focus:border-gold focus:outline-none"
                            />
                            <Button className="h-12">Subscribe</Button>
                        </div>
                    </CardContent>
                </Card>
            </section>
        </div>
    );
};

const BlogCard = ({ title, excerpt, author, date, category, slug }: typeof BLOG_POSTS[0]) => (
    <Card className="bg-temple/50 backdrop-blur-sm border-gold/10 hover:border-gold/40 group h-full flex flex-col">
        <div className="h-48 bg-gradient-to-br from-gold/20 to-temple flex items-center justify-center border-b border-gold/10">
            <div className="text-5xl">𓆣</div>
        </div>
        <CardHeader className="flex-1">
            <div className="flex items-center gap-2 mb-3">
                <Tag className="w-4 h-4 text-gold" />
                <span className="text-xs text-gold">{category}</span>
            </div>
            <CardTitle className="group-hover:text-gold transition-colors">
                {title}
            </CardTitle>
            <CardDescription className="text-base mt-3">
                {excerpt}
            </CardDescription>
        </CardHeader>
        <CardContent className="pt-0">
            <div className="flex items-center gap-4 text-xs text-sand mb-4">
                <div className="flex items-center gap-1">
                    <User className="w-3 h-3" />
                    {author}
                </div>
                <div className="flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    {date}
                </div>
            </div>
            <Link to={`/blog/${slug}`}>
                <Button variant="ghost" size="sm" className="group-hover:text-gold">
                    Read More <ArrowRight className="ml-2 w-4 h-4" />
                </Button>
            </Link>
        </CardContent>
    </Card>
);
