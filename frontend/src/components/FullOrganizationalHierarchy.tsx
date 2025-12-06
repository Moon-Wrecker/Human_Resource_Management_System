'use client';

import React, { useState, useEffect } from 'react';
import {
  type ReportingStructure,
  type UserHierarchyNode
} from '@/services/organizationService';

import { Tree, TreeNode } from 'react-organizational-chart';

import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { cn } from '@/lib/utils';

interface FullOrganizationalHierarchyProps {
  reportingStructure: ReportingStructure;
}

// ORG NODE (shadcn styled)
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'; // if you have shadcn avatar

const OrgNode: React.FC<{
  user: UserHierarchyNode;
  level: 'manager' | 'employee';
  isMe?: boolean;
}> = ({ user, level, isMe }) => {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Card
          className={cn(
            'max-w-xs rounded-lg p-4 w-full text-center cursor-pointer transition-shadow hover:shadow-lg',

            level === 'manager' && 'bg-gray-50 border border-gray-200',
            level === 'employee' && 'bg-white border border-gray-200',

            isMe && 'bg-blue-50 border-blue-400'
          )}
        >
          <div className="flex flex-col items-center space-y-2">
            <Avatar className="w-16 h-16">
              {user.profile_image ? (
                <AvatarImage src={user.profile_image} alt={user.name} />
              ) : (
                <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
              )}
            </Avatar>

            <div className="font-semibold text-lg">{user.name}</div>

            {user.position && (
              <div className="text-sm text-muted-foreground">{user.position}</div>
            )}

            {user.team && (
              <div className="text-xs text-muted-foreground">{user.team}</div>
            )}
          </div>
        </Card>
      </TooltipTrigger>
      <TooltipContent className="max-w-xs">
        <div className="space-y-1">
          <p className="font-semibold">{user.name}</p>
          {user.email && (
            <p className="text-sm">
              <span className="font-medium">Email:</span> {user.email}
            </p>
          )}
          {user.role && (
            <p className="text-sm">
              <span className="font-medium">Role:</span> {user.role}
            </p>
          )}
          {user.department && (
            <p className="text-sm">
              <span className="font-medium">Department:</span> {user.department}
            </p>
          )}
          {user.position && (
            <p className="text-sm">
              <span className="font-medium">Position:</span> {user.position}
            </p>
          )}
          {user.team && (
            <p className="text-sm">
              <span className="font-medium">Team:</span> {user.team}
            </p>
          )}
        </div>
      </TooltipContent>
    </Tooltip>
  );
};


const FullOrganizationalHierarchy: React.FC<
  FullOrganizationalHierarchyProps
> = ({ reportingStructure }) => {
  const { employee, direct_manager, peers } = reportingStructure;
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // simulate loading if needed
    setTimeout(() => setLoading(false), 250);
  }, []);

  if (loading) {
    return (
      <div className="p-10 text-center">
        <Skeleton className="w-64 h-6 mx-auto mb-6" />
        <Skeleton className="w-full h-40" />
      </div>
    );
  }

  return (
    <TooltipProvider>
      <div className="p-10 w-full overflow-auto">
        <h2 className="text-center mb-10 text-2xl font-bold">
          My Manager & Peers
        </h2>

        <ScrollArea className="w-full">
          {direct_manager ? (
            <Tree
              lineWidth="2px"
              lineColor="#000"
              lineBorderRadius="0"
              label={
                <div className="flex items-center justify-center w-full">
                 <OrgNode user={direct_manager} level="manager" />
                </div>
              }
            >
              <TreeNode
                label={<OrgNode user={employee} isMe level="employee" />}
              />

              {peers.map((peer) => (
                <TreeNode
                  key={peer.id}
                  label={<OrgNode user={peer} level="employee" />}
                />
              ))}
            </Tree>
          ) : (
            <div className="text-center">
              <OrgNode user={employee} isMe level="employee" />
              <p className="text-muted-foreground mt-3">
                No manager information available
              </p>
            </div>
          )}
        </ScrollArea>
      </div>
    </TooltipProvider>
  );
};

export default FullOrganizationalHierarchy;
