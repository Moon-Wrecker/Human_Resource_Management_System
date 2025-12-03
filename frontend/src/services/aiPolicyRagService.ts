/**
 * AI Policy RAG Service
 * Frontend service for Policy Q&A AI features
 */

import api from "./api";

// ==================== Types ====================

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface PolicyQuestion {
  question: string;
  chat_history?: ChatMessage[];
}

export interface PolicyAnswer {
  success: boolean;
  answer?: string;
  sources?: Array<{
    policy_title: string;
    content: string;
  }>;
  question?: string;
  error?: string;
}

export interface PolicySuggestions {
  suggestions: string[];
}

export interface PolicyIndexStatus {
  indexed: boolean;
  total_vectors?: number;
  index_location?: string;
  model?: string;
  embedding_model?: string;
  message?: string;
  error?: string;
}

// ==================== Service Functions ====================

/**
 * Ask a question about company policies
 */
export const askPolicyQuestion = async (
  data: PolicyQuestion,
): Promise<PolicyAnswer> => {
  try {
    const response = await api.post("/ai/policy-rag/ask", data);
    return response.data;
  } catch (error: any) {
    console.error("Error asking policy question:", error);
    return {
      success: false,
      error: error.response?.data?.detail || "Failed to get answer",
    };
  }
};

/**
 * Get suggested policy questions
 */
export const getPolicySuggestions = async (): Promise<string[]> => {
  try {
    const response = await api.get("/ai/policy-rag/suggestions");
    return response.data.suggestions || [];
  } catch (error: any) {
    console.error("Error getting suggestions:", error);
    return [];
  }
};

/**
 * Get policy index status
 */
export const getPolicyIndexStatus = async (): Promise<PolicyIndexStatus> => {
  try {
    const response = await api.get("/ai/policy-rag/status");
    return response.data;
  } catch (error: any) {
    console.error("Error getting index status:", error);
    return {
      indexed: false,
      error: error.response?.data?.detail || "Failed to get status",
    };
  }
};

/**
 * Rebuild policy index (admin only)
 */
export const rebuildPolicyIndex = async (): Promise<{ message: string }> => {
  try {
    const response = await api.post("/ai/policy-rag/index/rebuild");
    return response.data;
  } catch (error: any) {
    console.error("Error rebuilding index:", error);
    throw new Error(error.response?.data?.detail || "Failed to rebuild index");
  }
};

// ==================== Utility Functions ====================

/**
 * Format policy answer for display
 */
export const formatPolicyAnswer = (answer: PolicyAnswer): string => {
  if (!answer.success || !answer.answer) {
    return answer.error || "No answer available";
  }
  return answer.answer;
};

/**
 * Extract source citations from answer
 */
export const extractSourceCitations = (answer: PolicyAnswer): string[] => {
  if (!answer.sources || answer.sources.length === 0) {
    return [];
  }
  return answer.sources.map((source) => source.policy_title);
};

/**
 * Check if Policy RAG is available
 */
export const isPolicyRagAvailable = async (): Promise<boolean> => {
  try {
    const status = await getPolicyIndexStatus();
    return status.indexed;
  } catch {
    return false;
  }
};
