"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Loader2, Upload, Download, FileText } from "lucide-react";
import policyService, { type Policy } from "@/services/policyService";

const Policies = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [currentPolicy, setCurrentPolicy] = useState<Policy | null>(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Fetch current policy on mount
  useEffect(() => {
    fetchCurrentPolicy();
  }, []);

  const fetchCurrentPolicy = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await policyService.getPolicies({ limit: 1 });
      if (response.policies.length > 0) {
        setCurrentPolicy(response.policies[0]);
      } else {
        setCurrentPolicy(null);
      }
    } catch (err) {
      setError("Failed to load policy information");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!currentPolicy) return;

    try {
      setDownloading(true);
      setError(null);
      await policyService.downloadAndSavePolicyDocument(
        currentPolicy.id,
        `Company_Policy_v${currentPolicy.version}.pdf`
      );
      setSuccess("Policy downloaded successfully!");
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError("Failed to download policy document");
      console.error(err);
    } finally {
      setDownloading(false);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    // Validate file
    const validationError = policyService.validatePolicyFile(selectedFile, 10);
    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      setUploading(true);
      setError(null);
      setSuccess(null);

      let policy = currentPolicy;

      if (!policy) {
        // No policy exists - create first one
        policy = await policyService.createPolicy({
          title: "Company Policy",
          content: "Official Company Policy Document",
          version: "1.0",
          effective_date: new Date().toISOString().split("T")[0],
          category: "General",
          description: "Company-wide policies and procedures",
        });
      } else {
        // Policy exists - increment version
        const currentVersion = parseFloat(policy.version) || 1.0;
        const newVersion = (currentVersion + 1.0).toFixed(1);

        policy = await policyService.updatePolicy(policy.id, {
          version: newVersion,
          effective_date: new Date().toISOString().split("T")[0],
        });
      }

      // Upload document
      await policyService.uploadPolicyDocument(policy.id, selectedFile);

      // Refresh policy
      await fetchCurrentPolicy();
      setSelectedFile(null);

      setSuccess(
        `Policy uploaded successfully! Current version: ${policy.version}`
      );
      setTimeout(() => setSuccess(null), 5000);
    } catch (err: any) {
      setError(
        err?.response?.data?.detail || "Failed to upload policy document"
      );
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      {/* Page Title */}
      <h1 className="text-2xl font-bold mb-8">Company Policies</h1>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive" className="w-full max-w-xl mb-6">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Success Alert */}
      {success && (
        <Alert className="w-full max-w-xl mb-6 border-green-500 bg-green-50">
          <AlertDescription className="text-green-700">
            {success}
          </AlertDescription>
        </Alert>
      )}

      {/* Current Policy Info */}
      {currentPolicy && (
        <Card className="w-full max-w-xl mb-8">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <FileText className="w-5 h-5" />
              Current Policy Information
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex justify-between">
              <span className="font-medium">Version:</span>
              <span>{currentPolicy.version}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-medium">Effective Date:</span>
              <span>
                {new Date(currentPolicy.effective_date).toLocaleDateString()}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="font-medium">Last Updated:</span>
              <span>
                {new Date(currentPolicy.updated_at).toLocaleDateString()}
              </span>
            </div>
            {currentPolicy.has_document && (
              <div className="flex justify-between">
                <span className="font-medium">Document:</span>
                <span className="text-green-600">Available</span>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Download Section */}
      <div className="w-full max-w-xl mb-12">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold text-lg mb-1">
                  Download Current Policy
                </h3>
                <p className="text-sm text-muted-foreground">
                  {currentPolicy
                    ? `Version ${currentPolicy.version}`
                    : "No policy available"}
                </p>
              </div>
              <Button
                onClick={handleDownload}
                disabled={!currentPolicy?.has_document || downloading}
                className="gap-2"
              >
                {downloading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Downloading...
                  </>
                ) : (
                  <>
                    <Download className="w-4 h-4" />
                    Download
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Upload Section */}
      <h2 className="text-xl font-bold mb-6">Update Policy Document</h2>
      <div className="flex flex-col items-center mb-6 w-full max-w-xl">
        <label
          htmlFor="upload-policy-file"
          className="w-full h-48 border-2 border-dashed border-gray-300 flex flex-col items-center justify-center rounded-xl cursor-pointer bg-white hover:bg-gray-50 transition-colors"
        >
          <Upload className="w-12 h-12 mb-3 text-gray-400" />
          <span className="font-medium text-lg text-gray-700">
            {selectedFile
              ? selectedFile.name
              : "Click to upload policy document"}
          </span>
          <span className="text-sm text-gray-500 mt-2">
            PDF only, max 10MB
          </span>
          {currentPolicy && (
            <span className="text-xs text-gray-400 mt-1">
              Current version: {currentPolicy.version} → New version:{" "}
              {(parseFloat(currentPolicy.version) + 1.0).toFixed(1)}
            </span>
          )}
          <input
            id="upload-policy-file"
            type="file"
            accept=".pdf,application/pdf"
            className="hidden"
            onChange={(e) => {
              setError(null);
              setSelectedFile(e.target.files?.[0] ?? null);
            }}
          />
        </label>
      </div>

      <Button
        onClick={handleUpload}
        disabled={!selectedFile || uploading}
        size="lg"
        className="gap-2"
      >
        {uploading ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            Uploading...
          </>
        ) : (
          <>
            <Upload className="w-4 h-4" />
            {currentPolicy ? "Update Policy" : "Upload First Policy"}
          </>
        )}
      </Button>
    </div>
  );
};

export default Policies;
