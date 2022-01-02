import { Box, makeStyles, Tab } from '@material-ui/core';
import { TabContext, TabList, TabPanel } from '@material-ui/lab';
import React, { useState } from 'react';
import { Token } from '../Main';
import { StakeForm } from './StakeForm';
import { WalletBalance } from './WalletBalance';

interface YourWalletProps {
	supportedTokens: Array<Token>;
}

const useStyles = makeStyles((theme) => ({
	tabContent: {
		display: 'flex',
		flexDirection: 'column',
		alignItems: 'center',
		gap: theme.spacing(4)
	},
	box: {
		backgroundColor: 'white',
		borderRadius: '25px'
	},
	header: {
		color: 'white'
	}
}));

export const YourWallet = ({ supportedTokens }: YourWalletProps) => {
	const classes = useStyles();
	const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0);

	const handleChange = (_: React.ChangeEvent<{}>, newValue: string) => {
		setSelectedTokenIndex(parseInt(newValue));
	};

	return (
		<Box>
			<h1 className={classes.header}> Your Wallet! </h1>
			<Box className={classes.box}>
				<TabContext value={selectedTokenIndex.toString()}>
					<TabList onChange={handleChange} aria-label='stake form tabs'>
						{supportedTokens.map((token, index) => {
							return (
								<Tab label={token.name} value={index.toString()} key={index} />
							);
						})}
					</TabList>
					{supportedTokens.map((_, index) => {
						return (
							<TabPanel value={index.toString()} key={index}>
								<div className={classes.tabContent}>
									<WalletBalance token={supportedTokens[selectedTokenIndex]} />
									<StakeForm token={supportedTokens[selectedTokenIndex]} />
								</div>
							</TabPanel>
						);
					})}
				</TabContext>
			</Box>
		</Box>
	);
};
