import{_ as o,d as i,a as t,w as s,n as e,y as a}from"./c.a24dad9a.js";import"./c.fef57cf6.js";import{o as n}from"./index-67cb530c.js";import{o as l}from"./c.bc0ca5c5.js";import"./c.2fd5868c.js";import"./c.abbbe9de.js";let c=class extends e{render(){const o=void 0===this._valid?"":this._valid?"✅":"❌";return a`
      <esphome-process-dialog
        .heading=${`Validate ${this.configuration} ${o}`}
        .type=${"validate"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Install"
          @click=${this._openInstall}
        ></mwc-button>
      </esphome-process-dialog>
    `}_openEdit(){l(this.configuration)}_openInstall(){n(this.configuration)}_handleProcessDone(o){this._valid=0==o.detail}_handleClose(){this.parentNode.removeChild(this)}};o([i()],c.prototype,"configuration",void 0),o([t()],c.prototype,"_valid",void 0),c=o([s("esphome-validate-dialog")],c);
