import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Download, ArrowRight, CheckCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import policyService, { type Policy } from "@/services/policyService";
import { Badge } from "@/components/ui/badge";
import {
  askPolicyQuestion,
  type PolicyAnswer,
  type PolicyQuestion,
} from "@/services/aiPolicyRagService";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

const Policies = () => {
  const suggestions = [
    "How many casual leaves are allowed per year?",
    "What is the policy for sick leave?",
    "How do I enroll in the health insurance plan?",
  ];
  const [policies, setPolicies] = useState<Policy[]>();
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

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

  const fetchPolicies = () =>
    policyService.getActivePolicies().then((res) => setPolicies(res));

  useEffect(() => {
    fetchPolicies();
  }, []);

  return (
    <div className="w-full max-w-3xl mx-auto px-4 flex flex-col items-center justify-center gap-6 mt-10">
      <h2 className="text-3xl font-semibold text-center mt-8">Policies</h2>

      {/* Download Card */}
      <Card className="w-full">
        <CardHeader>
          {policies ? (
            policies.map((p) => (
              <CardTitle className="text-md flex items-center justify-between">
                <p className="flex items-center justify-start gap-2">
                  {p.title}
                  <Badge>v{p.version}</Badge>
                </p>
                <div className="flex items-center justify-end gap-2">
                  <div className="flex-1 w-full">
                    {!p.is_acknowledged_by_user ? (
                      <Button
                        className="flex items-center gap-2"
                        onClick={() => {
                          policyService.acknowledgePolicy(p.id);
                          fetchPolicies();
                        }}
                      >
                        <CheckCheck className="w-4 h-4" />
                        Acknowledge
                      </Button>
                    ) : (
                      <Button
                        variant="outline"
                        className="flex items-center gap-2"
                      >
                        Acknowledged
                      </Button>
                    )}
                  </div>
                  <a href={p.document_url}>
                    <Button
                      variant="outline"
                      className="flex items-center gap-2"
                    >
                      <Download className="w-4 h-4" />
                      Download
                    </Button>
                  </a>
                </div>
              </CardTitle>
            ))
          ) : (
            <CardContent>
              <p>No policy found</p>
            </CardContent>
          )}
        </CardHeader>
      </Card>

      <div className="font-semibold text-gray-500 text-sm uppercase tracking-widest">
        OR
      </div>

      {/* Ask About Policies Card */}
      <Card className="w-[60%]">
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
                      ? "bg-blue-500 text-white"
                      : "bg-gray-200"
                  }`}
                >
                  {message.content}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start mb-2">
                <div className="p-2 rounded-lg bg-gray-200">Typing...</div>
              </div>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-2 mt-2">
            {suggestions.map((s, i) => (
              <Button
                key={i}
                variant="outline"
                className="justify-start font-normal text-sm"
                onClick={() => handleSendMessage(s)}
              >
                {s}
              </Button>
            ))}
          </div>

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
