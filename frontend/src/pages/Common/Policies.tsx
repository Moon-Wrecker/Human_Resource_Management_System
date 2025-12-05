import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Download, ArrowRight, CheckCheck, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";
import { Badge } from "@/components/ui/badge";
import {
  askPolicyQuestion,
  type PolicyAnswer,
  type PolicyQuestion,
  getPolicySuggestions, // Imported getPolicySuggestions
} from "@/services/aiPolicyRagService";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { cn } from "@/lib/utils";
import policyService, { type Policy } from "@/services/policyService"; // Import policyService and Policy type

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

const Policies = () => {
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false); // Added state for collapsible
  const [currentPolicy, setCurrentPolicy] = useState<Policy | null>(null); // State for fetched policy
  const [isLoadingPolicy, setIsLoadingPolicy] = useState(true); // State for policy loading
  const [dynamicSuggestions, setDynamicSuggestions] = useState<string[]>([]); // State for dynamic suggestions
  const [isLoadingSuggestions, setIsLoadingSuggestions] = useState(true);

  // States for controlled suggestions animation
  const [showSuggestionsBlock, setShowSuggestionsBlock] = useState(true);
  const [renderSuggestionsBlock, setRenderSuggestionsBlock] = useState(true);
  const transitionDuration = 200; // ms, matches Tailwind's duration-200

  useEffect(() => {
    const fetchActivePolicy = async () => {
      try {
        setIsLoadingPolicy(true);
        const response = await policyService.getActivePolicies(1);
        if (response && response.length > 0) {
          setCurrentPolicy(response[0]);
        }
      } catch (error) {
        console.error("Error fetching active policy:", error);
      } finally {
        setIsLoadingPolicy(false);
      }
    };
    fetchActivePolicy();
  }, []);

  useEffect(() => {
    const fetchSuggestions = async () => {
      try {
        setIsLoadingSuggestions(true);
        const suggestions = await getPolicySuggestions();
        setDynamicSuggestions(suggestions);
      } catch (error) {
        console.error("Error fetching policy suggestions:", error);
      } finally {
        setIsLoadingSuggestions(false);
      }
    };
    fetchSuggestions();
  }, []);

  // Effect to control suggestions block visibility and rendering
  useEffect(() => {
    if (chatHistory.length > 0 && showSuggestionsBlock) {
      // Hide and then unmount
      setShowSuggestionsBlock(false);
      const timer = setTimeout(
        () => setRenderSuggestionsBlock(false),
        transitionDuration,
      );
      return () => clearTimeout(timer);
    } else if (
      chatHistory.length === 0 &&
      !showSuggestionsBlock &&
      !renderSuggestionsBlock
    ) {
      // Mount and then show
      setRenderSuggestionsBlock(true);
      const timer = setTimeout(() => setShowSuggestionsBlock(true), 10); // Small delay to allow element to mount
      return () => clearTimeout(timer);
    } else if (
      chatHistory.length === 0 &&
      !showSuggestionsBlock &&
      renderSuggestionsBlock
    ) {
      // If chat history is empty, and it's rendered but not shown, show it.
      setShowSuggestionsBlock(true);
    }
  }, [chatHistory.length, showSuggestionsBlock, renderSuggestionsBlock]);

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;

    const userMessage: ChatMessage = { role: "user", content: message };
    setChatHistory((prev) => [...prev, userMessage]);
    setQuestion("");
    setIsLoading(true);

    try {
      const policyQuestion: PolicyQuestion = {
        question: message,
        chat_history: chatHistory,
      };
      const result: PolicyAnswer = await askPolicyQuestion(policyQuestion);
      const assistantMessage: ChatMessage = {
        role: "assistant",
        content:
          result.answer || result.error || "Sorry, I could not find an answer.",
      };
      setChatHistory((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        role: "assistant",
        content: "An error occurred while fetching the answer.",
      };
      setChatHistory((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto px-4 flex flex-col items-center justify-center gap-6 mt-10">
      <h2 className="text-3xl font-semibold text-center mt-8">Policies</h2>

      {/* Policy Collapsible */}
      {isLoadingPolicy ? (
        <div className="w-full text-center p-4">Loading policy...</div>
      ) : currentPolicy ? (
        <Collapsible open={isOpen} onOpenChange={setIsOpen} className="w-full">
          <CollapsibleTrigger asChild>
            <div className="flex items-center justify-between w-full cursor-pointer py-2 px-4 rounded-md text-lg font-bold text-foreground">
              <span className="flex items-center gap-2">
                Our Company's policy
                <Badge>v{currentPolicy.version}</Badge>
              </span>
              <ChevronRight
                className={cn(
                  "h-4 w-4 transition-transform",
                  isOpen && "rotate-90",
                )}
              />
            </div>
          </CollapsibleTrigger>
          <CollapsibleContent className="data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 duration-200">
            <div className="mt-4 p-4 border rounded-md bg-gray-50">
              <div className="flex items-center justify-end mb-4">
                {" "}
                {/* Removed "Policy document embedded below." */}
                <div className="flex items-center gap-2">
                  {currentPolicy.document_url && (
                    <a
                      href={currentPolicy.document_url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <Button
                        variant="outline"
                        className="flex items-center gap-2"
                      >
                        <Download className="w-4 h-4" />
                        Download
                      </Button>
                    </a>
                  )}
                </div>
              </div>
              {currentPolicy.document_url ? (
                <div className="relative" style={{ paddingTop: "56.25%" }}>
                  {" "}
                  {/* 16:9 Aspect Ratio */}
                  <iframe
                    src={currentPolicy.document_url}
                    className="absolute top-0 left-0 w-full h-full"
                    title="Policy Document"
                    style={{ border: "none" }}
                  ></iframe>
                </div>
              ) : (
                <div className="space-y-4">
                  {currentPolicy.description && (
                    <div>
                      <h3 className="text-lg font-semibold">Description:</h3>
                      <p className="text-gray-800">
                        {currentPolicy.description}
                      </p>
                    </div>
                  )}
                  {currentPolicy.content && (
                    <div>
                      <h3 className="text-lg font-semibold">Content:</h3>
                      <div className="prose max-w-none">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {currentPolicy.content}
                        </ReactMarkdown>
                      </div>
                    </div>
                  )}
                  <div className="flex flex-wrap gap-4">
                    {currentPolicy.category && (
                      <div>
                        <h3 className="text-sm font-semibold text-gray-600">
                          Category:
                        </h3>
                        <Badge variant="secondary">
                          {currentPolicy.category}
                        </Badge>
                      </div>
                    )}
                    {currentPolicy.effective_date && (
                      <div>
                        <h3 className="text-sm font-semibold text-gray-600">
                          Effective Date:
                        </h3>
                        <p className="text-gray-800">
                          {policyService.formatDate(
                            currentPolicy.effective_date,
                          )}
                        </p>
                      </div>
                    )}
                    {currentPolicy.review_date && (
                      <div>
                        <h3 className="text-sm font-semibold text-gray-600">
                          Review Date:
                        </h3>
                        <p className="text-gray-800">
                          {policyService.formatDate(currentPolicy.review_date)}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </CollapsibleContent>
        </Collapsible>
      ) : (
        <div className="w-full text-center p-4">No active policy found.</div>
      )}

      <div className="font-semibold text-gray-500 text-sm uppercase tracking-widest">
        OR
      </div>

      {/* Ask About Policies Card */}
      <Card className="w-full max-w-4xl">
        <CardHeader className="flex flex-row justify-between items-start">
          <div>
            <CardTitle className="text-lg font-semibold">
              Ask about policies
            </CardTitle>
            <CardDescription>
              Get instant answers from your documents
            </CardDescription>
          </div>
          <Button variant="secondary" size="sm" className="text-xs font-medium">
            AI - Powered
          </Button>
        </CardHeader>

        <CardContent className="flex flex-col gap-3">
          <div className="flex flex-col h-64 overflow-y-auto p-4 border rounded-md">
            {chatHistory.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.role === "user" ? "justify-end" : "justify-start"
                } mb-2`}
              >
                <div
                  className={`p-2 rounded-lg ${
                    message.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-muted-foreground"
                  }`}
                >
                  {message.role === "assistant" ? (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {message.content}
                    </ReactMarkdown>
                  ) : (
                    message.content
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start mb-2">
                <div className="p-2 rounded-lg bg-muted text-muted-foreground">
                  Typing...
                </div>
              </div>
            )}
          </div>

          {renderSuggestionsBlock && (
            <div
              className={cn(
                "flex flex-wrap items-center gap-2 mt-2 transition-opacity duration-200",
                showSuggestionsBlock
                  ? "opacity-100"
                  : "opacity-0 h-0 overflow-hidden",
              )}
            >
              {isLoadingSuggestions ? (
                <div className="text-sm text-gray-500">
                  Loading suggestions...
                </div>
              ) : dynamicSuggestions.length > 0 ? (
                dynamicSuggestions.map((s, i) => (
                  <Button
                    key={i}
                    variant="outline"
                    className="justify-start font-normal text-sm transition-all duration-200"
                    onClick={() => handleSendMessage(s)}
                  >
                    {s}
                  </Button>
                ))
              ) : (
                <p className="text-sm text-gray-500">
                  No suggestions available.
                </p>
              )}
            </div>
          )}
          {chatHistory.length > 0 &&
            !renderSuggestionsBlock &&
            dynamicSuggestions.length > 0 && (
              <p className="text-sm text-gray-500 mt-2">
                Suggestions hidden during chat.
              </p>
            )}

          <div className="flex items-center gap-2 mt-2">
            <Input
              placeholder="Type your question..."
              className="flex-1"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === "Enter") {
                  handleSendMessage(question);
                }
              }}
            />
            <Button
              size="icon"
              variant="default"
              onClick={() => handleSendMessage(question)}
              disabled={isLoading}
            >
              <ArrowRight className="w-4 h-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Policies;

