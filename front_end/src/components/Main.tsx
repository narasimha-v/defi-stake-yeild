import { makeStyles } from '@material-ui/core';
import { useEthers } from '@usedapp/core';
import { constants } from 'ethers';
import brownieConfig from '../brownie-config.json';
import networkMapping from '../chain-info/deployments/map.json';
import helperConfig from '../helper-config.json';
import dai from '../images/dai.png';
import dapp from '../images/dapp.png';
import eth from '../images/eth.png';
import { YourWallet } from './yourWallet';

export type Token = {
	image: string;
	address: string;
	name: string;
};

const useStyles = makeStyles((theme) => ({
	title: {
		color: theme.palette.common.white,
		textAlign: 'center',
		padding: theme.spacing(4)
	}
}));

export const Main = () => {
	const classes = useStyles();
	const { chainId } = useEthers();
	const networkName = chainId ? helperConfig[chainId] : 'dev';
	let stringChainId = String(chainId);

	const dappTokenAddress = chainId
		? networkMapping[stringChainId]['DappToken'][0]
		: constants.AddressZero;

	const wethTokenAddress = chainId
		? brownieConfig['networks'][networkName]['weth_token']
		: constants.AddressZero;

	const fauTokenAddress = chainId
		? brownieConfig['networks'][networkName]['fau_token']
		: constants.AddressZero;

	const supportedTokens: Array<Token> = [
		{
			image: dapp,
			address: dappTokenAddress,
			name: 'DAPP'
		},
		{
			image: eth,
			address: wethTokenAddress,
			name: 'WETH'
		},
		{
			image: dai,
			address: fauTokenAddress,
			name: 'DAI'
		}
	];

	return (
		<>
			<h2 className={classes.title}>Dapp Token App</h2>
			<YourWallet supportedTokens={supportedTokens} />
		</>
	);
};
