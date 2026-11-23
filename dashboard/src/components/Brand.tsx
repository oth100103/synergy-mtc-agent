import { Sparkles } from "lucide-react";

// Synergy MTC Agent's mark, name and the dashboard's tagline, as the header and the
// sign-in page show them.
export function Brand() {
  return (
    <>
      <Sparkles />
      Synergy MTC <span className="tagline">Agent</span>
    </>
  );
}
