import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { MyEnrollment, SkillModule } from "@/services/skillService";
import skillService from "@/services/skillService";
import { ArrowRight, Search } from "lucide-react";
import { useEffect, useState, useRef } from "react";

const SkillDevelopment = () => {
  const [skillDevelopementItems, setSkillDevelopmentItems] = useState<
    SkillModule[]
  >([]);
  const [enrolledSkillDevelopementItems, setEnrolledSkillDevelopmentItems] =
    useState<MyEnrollment[]>();
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [search, setSearch] = useState("");
  const [difficulty, setDifficulty] = useState("");

  const prevSearch = useRef(search);
  const prevDifficulty = useRef(difficulty);

  useEffect(() => {
    const isFilterChanged =
      search !== prevSearch.current || difficulty !== prevDifficulty.current;

    if (isFilterChanged) {
      setPage(1);
    }

    const fetchModules = () => {
      setLoading(true);
      const filters = {
        page: isFilterChanged ? 1 : page,
        page_size: 6,
        search: search,
        difficulty: difficulty,
      };
      skillService
        .getModules(filters)
        .then((res) => {
          if (isFilterChanged || page === 1) {
            setSkillDevelopmentItems(res.modules);
          } else {
            setSkillDevelopmentItems((prev) => [...prev, ...res.modules]);
          }
          setHasMore(res.total_pages > (isFilterChanged ? 1 : page));
        })
        .catch((err) => console.error(err))
        .finally(() => {
          setLoading(false);
          prevSearch.current = search;
          prevDifficulty.current = difficulty;
        });
    };

    fetchModules();
  }, [page, search, difficulty]);

  useEffect(() => {
    skillService
      .getMyEnrollments()
      .then((res) => setEnrolledSkillDevelopmentItems(res))
      .catch((err) => console.error(err));
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      if (
        window.innerHeight + document.documentElement.scrollTop >=
          document.documentElement.offsetHeight - 20 &&
        hasMore &&
        !loading
      ) {
        setPage((prev) => prev + 1);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [loading, hasMore]);

  const submitSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // The useEffect will handle the search
  };

  const enrolledIds = new Set(
    enrolledSkillDevelopementItems?.map((en) => en.module_id),
  );

  const filteredModules = skillDevelopementItems.filter(
    (mod) => !enrolledIds.has(mod.id),
  );
  return (
    <div className="flex items-center justify-center flex-col">
      <h2 className="text-3xl font-semibold text-center my-8">
        Skill Developement Modules
      </h2>
      <div className="flex items-center justify-center w-[80%] gap-4 my-4">
        <form
          onSubmit={submitSearch}
          className="flex-grow flex items-center gap-1"
        >
          <Input
            placeholder="Search... "
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <Button type="submit" variant="outline">
            <Search />
          </Button>
        </form>
        <Select value={difficulty} onValueChange={setDifficulty}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Difficulty" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="beginner">Beginner</SelectItem>
            <SelectItem value="intermediate">Intermediate</SelectItem>
            <SelectItem value="advanced">Advanced</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {enrolledSkillDevelopementItems?.length && (
        <>
          <h2 className="text-2xl font-bold pt-8">My Enrollments</h2>
          <div className="w-[70%] grid grid-cols-3 my-8 px-4 gap-4">
            {enrolledSkillDevelopementItems.map((skillDevelopementItem) => (
              <Card
                key={skillDevelopementItem.id}
                className="w-full max-w-md shadow-md rounded-2xl border border-gray-200"
              >
                <CardHeader>
                  <CardTitle className="text-lg font-semibold text-gray-900">
                    {skillDevelopementItem.module_name}
                  </CardTitle>
                </CardHeader>

                <CardContent className="h-full align-text-top">
                  <p className="text-gray-700 text-sm leading-relaxed h-full">
                    {skillDevelopementItem.module_description}
                  </p>
                </CardContent>

                <CardFooter className="flex justify-end">
                  <Button
                    asChild
                    variant="outline"
                    className="flex items-center gap-2"
                  >
                    <a
                      href={`/employee/skills/${skillDevelopementItem.module_id}`}
                    >
                      View Details
                      <ArrowRight className="w-4 h-4" />
                    </a>
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        </>
      )}

      {filteredModules?.length > 0 ? (
        <>
          <h2 className="text-2xl font-bold pt-8">New Courses</h2>
          <div className="w-[70%] grid grid-cols-3 my-8 px-4 gap-4">
            {filteredModules.map((skillDevelopementItem) => (
              <Card
                key={skillDevelopementItem.id}
                className="w-full max-w-md shadow-md rounded-2xl border border-gray-200"
              >
                <CardHeader>
                  <CardTitle className="text-lg font-semibold text-gray-900">
                    {skillDevelopementItem.name}
                  </CardTitle>
                </CardHeader>

                <CardContent className="h-full align-text-top">
                  <p className="h-full text-gray-700 text-sm leading-relaxed">
                    {skillDevelopementItem.description}
                  </p>
                </CardContent>

                <CardFooter className="flex justify-end">
                  <Button
                    className="flex items-center gap-2 cursor-pointer"
                    onClick={() =>
                      skillService.enrollInModule({
                        module_id: skillDevelopementItem.id,
                      })
                    }
                  >
                    Enroll Now
                    <ArrowRight className="w-4 h-4" />
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        </>
      ) : (
        !loading && <p>No skill modules found.</p>
      )}
      {loading && <p>Loading...</p>}
    </div>
  );
};

export default SkillDevelopment;
