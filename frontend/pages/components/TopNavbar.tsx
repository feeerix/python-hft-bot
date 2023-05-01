import Link from "next/link";
import { Navbar, Button, Grid, Switch } from '@nextui-org/react';

type NavbarProps = {
    links: {
      href: string;
      label: string;
    }[];
    isDarkMode: boolean;
    handleToggleDarkMode: () => void;
  };
  
const TopNavbar: React.FC<NavbarProps> = ({ 
    links,
    isDarkMode,
    handleToggleDarkMode
}) => {
    return (
      <Navbar variant={"static"} maxWidth={"fluid"}>
        <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
            <Grid.Container gap={1}>
                {links.map((link) => (
                    <Grid key={link.label}>
                        <Link href={link.href}>
                            <Button auto type="button">
                                    {link.label}
                            </Button>
                        </Link>
                    </Grid>
                ))}
            </Grid.Container>
        </div>
        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                
                <Grid.Container gap={1}>
                    <Grid>
                        <Switch checked={isDarkMode} onChange={handleToggleDarkMode} />
                    </Grid>
                </Grid.Container>
                
            </div>
      </Navbar>
    );
  };
  
  export default TopNavbar;