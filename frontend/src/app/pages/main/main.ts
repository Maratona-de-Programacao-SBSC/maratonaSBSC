import { Component } from '@angular/core';
import { HeroSection } from "../../components/hero-section/hero-section";
import { Sobre } from "../../components/sobre/sobre";

@Component({
  selector: 'app-main',
  imports: [HeroSection, Sobre],
  templateUrl: './main.html',
  styleUrl: './main.scss',
})
export class Main {}
