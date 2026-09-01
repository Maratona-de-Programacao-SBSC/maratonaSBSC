import { ChangeDetectionStrategy, Component } from '@angular/core';
import { HeroSection } from '../../components/hero-section/hero-section';
import { Sobre } from '../../components/sobre/sobre';
import { ExplicacoesComponent } from '../../components/explicacao/explicacao';

@Component({
  selector: 'app-main',
  imports: [HeroSection, Sobre, ExplicacoesComponent],
  templateUrl: './main.html',
  styleUrl: './main.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Main {}
