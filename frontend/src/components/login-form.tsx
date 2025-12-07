import AppLogoName from "../assets/app-logo-name.svg"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { useState, type FormEvent } from "react"
import { useAuth } from "@/contexts/AuthContext"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"div">) {
  const { login, isLoading } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [showForgotPasswordModal, setShowForgotPasswordModal] = useState(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    // Validation
    if (!email || !password) {
      setError("Please enter both email and password");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    try {
      await login(email, password);
      // Navigation is handled by AuthContext based on role
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed. Please check your credentials.");
    }
  };

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card className="overflow-hidden p-0">
        <CardContent className="grid p-0 md:grid-cols-2">
          <form className="p-6 md:p-8" onSubmit={handleSubmit}>
            <FieldGroup>
              <div className="flex flex-col items-center gap-2 text-center">
                <h1 className="text-2xl font-bold">Welcome back</h1>
                <p className="text-muted-foreground text-balance">
                  Login to your PulseTrack Account
                </p>
              </div>
              
              {error && (
                <div className="rounded-md bg-red-50 p-4 text-sm text-red-800 border border-red-200">
                  {error}
                </div>
              )}

              <Field>
                <FieldLabel htmlFor="email">Email</FieldLabel>
                <Input
                  id="email"
                  type="email"
                  placeholder="m@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  disabled={isLoading}
                />
              </Field>
              <Field>
                <div className="flex items-center">
                  <FieldLabel htmlFor="password">Password</FieldLabel>
                  <Dialog open={showForgotPasswordModal} onOpenChange={setShowForgotPasswordModal}>
                    <DialogTrigger asChild>
                      <a
                        href="#"
                        onClick={(e) => {
                          e.preventDefault();
                          setShowForgotPasswordModal(true);
                        }}
                        className="ml-auto text-sm underline-offset-2 hover:underline"
                      >
                        Forgot your password?
                      </a>
                    </DialogTrigger>
                    <DialogContent className="p-6">
                      <DialogHeader>
                        <DialogTitle>Password Reset Information</DialogTitle>
                        <DialogDescription>
                          To reset your password, please contact your HR department directly.
                          <br /><br />
                          They will be able to assist you with the process and ensure your account security.
                          <br /><br />
                          Thank you for your understanding.
                        </DialogDescription>
                      </DialogHeader>
                    </DialogContent>
                  </Dialog>
                </div>
                <Input 
                  id="password" 
                  type="password" 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  disabled={isLoading}
                />
              </Field>
              <Field>
                <Button type="submit" disabled={isLoading}>
                  {isLoading ? "Logging in..." : "Login"}
                </Button>
              </Field>
              
              {/* Test credentials hint */}
              <div className="rounded-md bg-blue-50 p-4 text-xs text-blue-800 border border-blue-200">
                <p className="font-semibold mb-1">Test Credentials:</p>
                <p>HR: sarah.johnson@company.com / pass123</p>
                <p>Manager: michael.chen@company.com / pass123</p>
                <p>Employee: john.doe@company.com / pass123</p>
              </div>


            </FieldGroup>
          </form>
          <div className="hidden flex-col items-center justify-center p-1 md:flex bg-gradient-to-br from-gray-400 to-white-600">
            <img src={AppLogoName} alt="App Logo" className="w-2/3 h-auto" />
          </div>
        </CardContent>
      </Card>
      <FieldDescription className="px-6 text-center">
        By clicking continue, you agree to our <a href="#">Terms of Service</a>{" "}
        and <a href="#">Privacy Policy</a>.
      </FieldDescription>
    </div>
  )
}
