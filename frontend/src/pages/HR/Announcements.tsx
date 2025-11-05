"use client";

import { useState } from "react";

// Announcement type
type AnnouncementLink = { text: string; url: string };
type AnnouncementData = {
  id: number;
  title: string;
  desc: string;
  links: AnnouncementLink[];
};

// Dialog Props type
interface AddAnnouncementDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (data: { title: string; desc: string; links: AnnouncementLink[] }) => void;
}

// Add Announcement Dialog Component
const AddAnnouncementDialog = ({
  open,
  onClose,
  onSave,
}: AddAnnouncementDialogProps) => {
  const [title, setTitle] = useState<string>("");
  const [desc, setDesc] = useState<string>("");
  const [links, setLinks] = useState<AnnouncementLink[]>([]);
  const [addingLink, setAddingLink] = useState<boolean>(false);
  const [newLinkText, setNewLinkText] = useState<string>("");
  const [newLinkUrl, setNewLinkUrl] = useState<string>("");

  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-20 flex items-center justify-center z-50">
      <div className="bg-[#e9e9ea] rounded-2xl w-[500px] shadow-xl relative p-2">
        <div className="flex items-center justify-between px-5 pt-4 pb-3 border-b">
          <span className="font-medium text-lg">Add Announcement</span>
          <button onClick={onClose} className="w-7 h-7 flex items-center justify-center text-xl hover:bg-gray-300 rounded-full">
            ×
          </button>
        </div>
        <form
          className="p-6 flex flex-col gap-6"
          onSubmit={e => {
            e.preventDefault();
            onSave({ title, desc, links });
            setTitle(""); setDesc(""); setLinks([]);
          }}
        >
          <div>
            <label className="block font-medium mb-2">Title:</label>
            <input
              type="text"
              className="w-full rounded bg-white border px-4 py-2"
              placeholder="Announce something..."
              value={title}
              onChange={e => setTitle(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block font-medium mb-2">Description:</label>
            <textarea
              className="w-full rounded bg-white border px-4 py-2 resize-none"
              rows={3}
              placeholder="Add Announcement Description..."
              value={desc}
              onChange={e => setDesc(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block font-medium underline mb-2">
              Links (optional):
            </label>
            {links.length > 0 && (
              <ul className="mb-2">
                {links.map((l, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-sm">
                    <a href={l.url} className="underline text-blue-600" target="_blank" rel="noopener noreferrer">
                      {l.text || l.url}
                    </a>
                    <button
                      type="button"
                      onClick={() => setLinks(links.filter((_, i) => i !== idx))}
                      className="ml-1 text-gray-500 hover:text-red-600 px-1"
                    >
                      ×
                    </button>
                  </li>
                ))}
              </ul>
            )}
            {addingLink ? (
              <div className="flex gap-2 items-center mb-2">
                <input
                  type="text"
                  className="border rounded px-2 py-1 w-24"
                  placeholder="Text"
                  value={newLinkText}
                  onChange={e => setNewLinkText(e.target.value)}
                />
                <input
                  type="url"
                  className="border rounded px-2 py-1"
                  placeholder="https://example.com"
                  value={newLinkUrl}
                  onChange={e => setNewLinkUrl(e.target.value)}
                />
                <button
                  type="button"
                  className="text-sm bg-blue-100 px-2 rounded hover:bg-blue-200"
                  onClick={() => {
                    if (newLinkUrl) {
                      setLinks([...links, { text: newLinkText, url: newLinkUrl }]);
                      setNewLinkText("");
                      setNewLinkUrl("");
                      setAddingLink(false);
                    }
                  }}
                >
                  Add
                </button>
                <button
                  type="button"
                  className="text-gray-400 hover:text-gray-600 ml-2"
                  onClick={() => {
                    setAddingLink(false);
                    setNewLinkText("");
                    setNewLinkUrl("");
                  }}
                >
                  ×
                </button>
              </div>
            ) : (
              <button
                type="button"
                className="text-sm underline hover:text-blue-600"
                onClick={() => setAddingLink(true)}
              >
                + Add link
              </button>
            )}
          </div>
          <div className="flex justify-end">
            <button
              type="submit"
              className="bg-gray-300 px-7 py-2 rounded font-semibold hover:bg-gray-400 transition flex items-center gap-1"
            >
              Save <span className="ml-1">&rarr;</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const initialAnnouncements: AnnouncementData[] = [
  {
    id: 1,
    title: "Quarterly Town Hall Scheduled",
    desc: "Our next company-wide town hall will be on 24th Nov. All team leads, please prepare your quarterly summaries for presentation.",
    links: [{ text: "Meeting details", url: "#" }]
  },
  {
    id: 2,
    title: "New HR Policy Update",
    desc: "Please review the updated HR leave policies. These come into effect from Dec 1. Contact HR for clarifications.",
    links: [{ text: "View Policy", url: "/hr-policies" }]
  },
  {
    id: 3,
    title: "Monthly Upskilling Webinar Series",
    desc: "We’re starting monthly webinars on advanced React.js topics. Everyone is welcome!",
    links: [
      { text: "Schedule", url: "#" },
      { text: "Register", url: "#" }
    ]
  },
  {
    id: 4,
    title: "Office Closed for Holiday",
    desc: "Our office will be closed on 12th Nov for Diwali. We wish everyone a happy and safe festival!",
    links: []
  }
];

const AnnouncementsContent = () => {
  const [showDialog, setShowDialog] = useState<boolean>(false);
  const [announcements, setAnnouncements] = useState<AnnouncementData[]>(initialAnnouncements);

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      <AddAnnouncementDialog
        open={showDialog}
        onClose={() => setShowDialog(false)}
        onSave={data => {
          setAnnouncements([
            ...announcements,
            { id: Date.now(), ...data }
          ]);
          setShowDialog(false);
        }}
      />
      <div className="flex w-full max-w-4xl items-center justify-between mb-10">
        <h1 className="text-2xl font-bold">Announcements</h1>
        <button
          onClick={() => setShowDialog(true)}
          className="font-medium underline text-base hover:opacity-80 transition"
        >
          Create New &rarr;
        </button>
      </div>
      <div className="w-full max-w-4xl grid grid-cols-1 sm:grid-cols-2 gap-8">
        {announcements.map((a) => (
          <div
            key={a.id}
            className="w-full min-h-[150px] bg-white shadow border rounded-lg p-5 flex flex-col"
          >
            <div className="font-bold text-lg mb-2">{a.title}</div>
            <div className="text-gray-700 mb-3 whitespace-pre-line">{a.desc}</div>
            {a.links && a.links.length > 0 && (
              <div className="flex flex-wrap gap-3 mt-auto">
                {a.links.map(link => (
                  <a
                    key={link.url}
                    href={link.url}
                    className="underline text-blue-600 hover:text-blue-800 font-medium text-sm"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {link.text} &rarr;
                  </a>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AnnouncementsContent;
